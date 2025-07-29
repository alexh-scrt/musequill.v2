#!/usr/bin/env python3
"""
Musequill Wizard Development Launcher
Starts both the FastAPI backend and serves the UI for development
"""

import os
import sys
import subprocess
import webbrowser
import signal
import time
from pathlib import Path
from threading import Thread

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class WizardLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = project_root
        
    def check_requirements(self):
        """Check if required dependencies are available"""
        print("🔍 Checking requirements...")
        
        # Check Python dependencies
        try:
            import uvicorn
            import fastapi
            import alpinejs  # This would be a custom check
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("💡 Install with: pip install -r requirements.txt")
            return False
            
        # Check if Ollama is running (optional check)
        try:
            import requests
            response = requests.get("http://localhost:11434/api/version", timeout=2)
            if response.status_code == 200:
                print("✅ Ollama service detected")
            else:
                print("⚠️  Ollama service not detected (optional)")
        except:
            print("⚠️  Ollama service not detected (optional)")
            
        print("✅ Requirements check complete")
        return True
        
    def start_backend(self):
        """Start the FastAPI backend"""
        print("🚀 Starting FastAPI backend...")
        
        backend_path = self.project_root / "musequill" / "services" / "frontend"
        
        try:
            # Change to the backend directory
            os.chdir(backend_path)
            
            # Start the backend
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
               universal_newlines=True, bufsize=1)
            
            # Monitor backend startup
            def monitor_backend():
                for line in self.backend_process.stdout:
                    print(f"[Backend] {line.strip()}")
                    
            backend_thread = Thread(target=monitor_backend, daemon=True)
            backend_thread.start()
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            # Check if backend is running
            if self.backend_process.poll() is None:
                print("✅ Backend started successfully on http://localhost:8000")
                return True
            else:
                print("❌ Backend failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
            
    def start_frontend(self):
        """Start the frontend development server"""
        print("🌐 Starting frontend server...")
        
        ui_path = self.project_root / "ui"
        
        try:
            # Try different servers in order of preference
            servers = [
                (["python", "-m", "http.server", "8080"], "Python HTTP Server"),
                (["python3", "-m", "http.server", "8080"], "Python3 HTTP Server"),
                (["npx", "serve", ".", "-p", "8080"], "Serve (Node.js)"),
                (["php", "-S", "localhost:8080"], "PHP Development Server")
            ]
            
            os.chdir(ui_path)
            
            for server_cmd, server_name in servers:
                try:
                    self.frontend_process = subprocess.Popen(
                        server_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                    )
                    
                    # Wait a moment to see if it starts
                    time.sleep(1)
                    
                    if self.frontend_process.poll() is None:
                        print(f"✅ Frontend started with {server_name} on http://localhost:8080")
                        return True
                    else:
                        continue
                        
                except FileNotFoundError:
                    continue
                    
            print("❌ Could not start any frontend server")
            print("💡 Please install Python, Node.js, or PHP to serve the frontend")
            return False
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
        finally:
            os.chdir(self.project_root)
            
    def open_browser(self):
        """Open the wizard in the default browser"""
        print("🌐 Opening wizard in browser...")
        try:
            webbrowser.open("http://localhost:8080")
            print("✅ Browser opened successfully")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("💡 Please open http://localhost:8080 manually")
            
    def show_status(self):
        """Show current status and helpful information"""
        print("\n" + "="*60)
        print("🎉 Musequill Wizard is now running!")
        print("="*60)
        print(f"📚 Frontend (Wizard UI): http://localhost:8080")
        print(f"⚙️  Backend (API):       http://localhost:8000")
        print(f"📖 API Docs:           http://localhost:8000/docs")
        print(f"🔍 Health Check:       http://localhost:8000/health")
        print("="*60)
        print("\n💡 Development Tips:")
        print("   • Edit files in ui/ to modify the wizard interface")
        print("   • Backend API documentation available at /docs")
        print("   • Check backend logs above for any issues")
        print("   • Press Ctrl+C to stop all services")
        print("\n🐛 Troubleshooting:")
        print("   • If wizard doesn't load, check console for errors")
        print("   • Ensure Ollama is running for LLM features")
        print("   • Check that ports 8000 and 8080 are available")
        
    def cleanup(self):
        """Clean up processes on exit"""
        print("\n🛑 Shutting down services...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except:
                self.backend_process.kill()
                print("🔥 Backend force-stopped")
                
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except:
                self.frontend_process.kill()
                print("🔥 Frontend force-stopped")
                
        print("👋 Goodbye!")
        
    def run(self):
        """Main launcher method"""
        print("🎭 Musequill Wizard Launcher")
        print("=" * 40)
        
        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            self.cleanup()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Check requirements
            if not self.check_requirements():
                return 1
                
            # Start backend
            if not self.start_backend():
                print("❌ Failed to start backend. Exiting.")
                return 1
                
            # Start frontend
            if not self.start_frontend():
                print("❌ Failed to start frontend. Exiting.")
                return 1
                
            # Open browser
            time.sleep(2)  # Give servers time to fully start
            self.open_browser()
            
            # Show status
            self.show_status()
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
                    
                    # Check if processes are still running
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("❌ Backend process died unexpectedly")
                        break
                        
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("❌ Frontend process died unexpectedly")
                        break
                        
            except KeyboardInterrupt:
                pass
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return 1
        finally:
            self.cleanup()
            
        return 0


def main():
    """Main entry point"""
    launcher = WizardLauncher()
    return launcher.run()


if __name__ == "__main__":
    sys.exit(main())