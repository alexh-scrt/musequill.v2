"""
IP Blacklisting Middleware

This middleware tracks invalid requests per IP address and blacklists IPs 
that make more than 3 invalid requests. Invalid requests include:
- 400 Bad Request
- 404 Not Found
- 422 Validation Error
- Any request that raises an HTTPException with these status codes

Usage:
    from .ip_blacklist_middleware import IPBlacklistMiddleware
    
    app = FastAPI()
    middleware = IPBlacklistMiddleware(app, max_violations=3, blacklist_duration_hours=24)
    app.add_middleware(type(middleware), **middleware.__dict__)
"""

import logging
import time
from collections import defaultdict, deque
from typing import Dict, Set, Tuple
from datetime import datetime, timedelta

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class IPBlacklistMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track and blacklist IPs that make too many invalid requests.
    
    Features:
    - Tracks invalid requests per IP address
    - Blacklists IPs after configurable number of violations
    - Time-based cleanup of old violations
    - Configurable blacklist duration
    - Comprehensive logging of blacklist events
    - Support for proxy headers (X-Forwarded-For, X-Real-IP)
    """
    
    def __init__(self, app, max_violations: int = 3, blacklist_duration_hours: int = 24):
        super().__init__(app)
        self.max_violations = max_violations
        self.blacklist_duration = timedelta(hours=blacklist_duration_hours)
        
        # Track violations per IP: {ip: [timestamp1, timestamp2, ...]}
        self.ip_violations: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10))
        
        # Blacklisted IPs with expiration time: {ip: expiration_datetime}
        self.blacklisted_ips: Dict[str, datetime] = {}
        
        # Track when we last cleaned up old data
        self.last_cleanup = datetime.now()
        self.cleanup_interval = timedelta(hours=1)
        
        logger.info(f"IP Blacklist middleware initialized: max_violations={max_violations}, "
                   f"blacklist_duration={blacklist_duration_hours}h")
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request, considering proxy headers."""
        # Check X-Forwarded-For header (for proxies/load balancers)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain (the original client)
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header (common with nginx)
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # Fall back to direct connection IP
        return request.client.host if request.client else "unknown"
    
    def _is_blacklisted(self, ip: str) -> bool:
        """Check if an IP is currently blacklisted."""
        if ip not in self.blacklisted_ips:
            return False
        
        # Check if blacklist has expired
        if datetime.now() > self.blacklisted_ips[ip]:
            del self.blacklisted_ips[ip]
            logger.info(f"IP {ip} blacklist expired and removed")
            return False
        
        return True
    
    def _record_violation(self, ip: str, status_code: int, path: str):
        """Record a violation for an IP address."""
        now = datetime.now()
        
        # Add violation timestamp
        self.ip_violations[ip].append(now)
        
        # Count recent violations (within the last hour)
        recent_violations = sum(1 for timestamp in self.ip_violations[ip] 
                              if now - timestamp < timedelta(hours=1))
        
        logger.warning(f"IP {ip} violation recorded: status={status_code}, path={path}, "
                      f"recent_violations={recent_violations}")
        
        # Check if we should blacklist this IP
        if recent_violations >= self.max_violations:
            expiration = now + self.blacklist_duration
            self.blacklisted_ips[ip] = expiration
            
            logger.error(f"IP {ip} BLACKLISTED until {expiration} "
                        f"(exceeded {self.max_violations} violations)")
            
            # You could add additional actions here, such as:
            # - Sending alerts to monitoring systems
            # - Updating external firewall rules
            # - Logging to security systems
    
    def _cleanup_old_data(self):
        """Remove old violation records to prevent memory bloat."""
        now = datetime.now()
        
        # Only cleanup periodically
        if now - self.last_cleanup < self.cleanup_interval:
            return
        
        self.last_cleanup = now
        cutoff_time = now - timedelta(hours=24)  # Keep 24 hours of history
        
        # Clean up old violations
        for ip in list(self.ip_violations.keys()):
            # Remove old timestamps
            violations = self.ip_violations[ip]
            while violations and violations[0] < cutoff_time:
                violations.popleft()
            
            # Remove empty entries
            if not violations:
                del self.ip_violations[ip]
        
        # Clean up expired blacklists (already done in _is_blacklisted)
        expired_ips = [ip for ip, expiration in self.blacklisted_ips.items() 
                      if now > expiration]
        for ip in expired_ips:
            del self.blacklisted_ips[ip]
        
        if expired_ips:
            logger.info(f"Cleaned up {len(expired_ips)} expired blacklist entries")
    
    def _is_invalid_status(self, status_code: int) -> bool:
        """Determine if a status code represents an invalid request."""
        # These status codes indicate client errors that should count as violations
        return status_code in {
            400,  # Bad Request - malformed request
            404,  # Not Found - invalid endpoint
            422,  # Unprocessable Entity - validation errors
            405,  # Method Not Allowed - wrong HTTP method
            406,  # Not Acceptable - invalid Accept header
        }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and apply IP blacklisting logic."""
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Skip blacklisting for health check endpoints to avoid blocking monitoring
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # Periodic cleanup
        self._cleanup_old_data()
        
        # Check if IP is blacklisted
        if self._is_blacklisted(client_ip):
            logger.warning(f"Blocked request from blacklisted IP {client_ip} to {request.url.path}")
            return JSONResponse(
                status_code=429,  # Too Many Requests
                content={
                    "success": False,
                    "error": "IP address is temporarily blacklisted due to repeated invalid requests",
                    "message": "Your IP has been temporarily blocked. Please try again later.",
                    "details": {
                        "blocked_until": self.blacklisted_ips[client_ip].isoformat(),
                        "reason": f"Exceeded {self.max_violations} invalid requests"
                    }
                }
            )
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Check if this was an invalid request
            if self._is_invalid_status(response.status_code):
                self._record_violation(client_ip, response.status_code, request.url.path)
            
            return response
            
        except HTTPException as http_exc:
            # Record violations for HTTP exceptions
            if self._is_invalid_status(http_exc.status_code):
                self._record_violation(client_ip, http_exc.status_code, request.url.path)
            
            # Re-raise the exception to maintain normal error handling
            raise http_exc
            
        except Exception as exc:
            # For unexpected errors (500s), don't count as violations
            # since these are typically server-side issues, not client errors
            logger.error(f"Unexpected error for IP {client_ip}: {exc}")
            raise exc
    
    def get_blacklist_status(self) -> Dict:
        """Get current blacklist status for monitoring/debugging."""
        now = datetime.now()
        
        active_blacklists = {
            ip: {
                "expires_at": expiration.isoformat(),
                "expires_in_minutes": int((expiration - now).total_seconds() / 60)
            }
            for ip, expiration in self.blacklisted_ips.items()
            if expiration > now
        }
        
        violation_counts = {
            ip: len([v for v in violations if now - v < timedelta(hours=1)])
            for ip, violations in self.ip_violations.items()
        }
        
        return {
            "active_blacklists": active_blacklists,
            "recent_violations": {ip: count for ip, count in violation_counts.items() if count > 0},
            "total_tracked_ips": len(self.ip_violations),
            "config": {
                "max_violations": self.max_violations,
                "blacklist_duration_hours": self.blacklist_duration.total_seconds() / 3600
            }
        }
    
    def remove_ip_from_blacklist(self, ip: str) -> bool:
        """Manually remove an IP from the blacklist. Returns True if IP was blacklisted."""
        if ip in self.blacklisted_ips:
            del self.blacklisted_ips[ip]
            logger.info(f"IP {ip} manually removed from blacklist")
            return True
        return False
    
    def add_ip_to_blacklist(self, ip: str, duration_hours: int = None) -> None:
        """Manually add an IP to the blacklist."""
        duration = timedelta(hours=duration_hours) if duration_hours else self.blacklist_duration
        expiration = datetime.now() + duration
        self.blacklisted_ips[ip] = expiration
        logger.warning(f"IP {ip} manually added to blacklist until {expiration}")