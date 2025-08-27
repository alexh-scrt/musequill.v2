from __future__ import annotations
from typing import List, Dict, Any
import json
import pathlib
import env
from book_plan import plan_book
from chapter_planner import make_all_chapter_briefs_from_plan
from chapter_writer  import write_all_chapters_with_qc
from poc.llm_ollama import llm
from poc.qa_session import QASession

def run_book_planning(
    model_path: str,
    blueprint_path: str,
    research_path: str,
    planning_txt_path: str,
    summary_txt_path: str,
    out_path: str
):
    with open(model_path, "r", encoding="utf-8") as f:
        book_model = json.load(f)
    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint = json.load(f)
    with open(research_path, "r", encoding="utf-8") as f:
        research = json.load(f)
    planning_text = pathlib.Path(planning_txt_path).read_text(encoding="utf-8")
    summary_text  = pathlib.Path(summary_txt_path).read_text(encoding="utf-8")


    plan = plan_book(
        book_model=book_model,
        blueprint=blueprint,
        research=research,
        planning_text=planning_text,
        summary_text=summary_text,
        max_total_words=60000,          # or 50000
        expected_chapters=24            # optional; defaults to 24 with 12/9/3 split
    )

    pathlib.Path(out_path).write_text(
        json.dumps(plan, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    briefs: List[Dict[str, Any]] = []
    try:
        briefs = make_all_chapter_briefs_from_plan(book_plan=plan, research_corpus=research)
        for chapter in briefs:
            pathlib.Path(f"design/samples/chapter-{chapter['meta']['chapter_number']}-brief.txt").write_text(
                json.dumps(chapter, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

    except Exception as e:
        print(f"Error in chapter planning: {e}")
        return

def run_chapter_planning(
    book_plan_path: str,
    research_path: str,
    summary_path: str,
    out_path: str
):
    with open(research_path, "r", encoding="utf-8") as f:
        research = json.load(f)
    with open(book_plan_path, "r", encoding="utf-8") as f:
        book_plan = json.load(f)
    with open(summary_path, "r", encoding="utf-8") as f:
        book_summary = f.read().strip()

    briefs: List[Dict[str, Any]] = []
    try:

        qa = QASession(llm_fn=llm)  # or your preferred local model
        qa.add_context("book_summary", book_summary)

        main_character = qa.ask("Who is the main character in the book?")

        character_description = qa.ask("Describe the main character in one sentence.")

        book_plan["canon"]["book_model"]['characters']['main_character'] = f'{main_character} - {character_description}'

        briefs = make_all_chapter_briefs_from_plan(book_plan=book_plan, research_corpus=research)
        for chapter in briefs:
            pathlib.Path(f"{out_path}/chapter-{chapter['meta']['chapter_number']}-brief.txt").write_text(
                json.dumps(chapter, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

        book_summary = f'Main character: {main_character} - {character_description}\n{book_plan["constraints"]["summary"]}'

        book_plan["constraints"]["summary"] = book_summary

        results = write_all_chapters_with_qc(
            book_plan=book_plan,
            chapter_briefs=briefs,          # output from your chapter planner
            research_corpus=research,
            llm=llm,
            out_dir="manuscript"
        )

        print('-- DONE --')
    except Exception as e:
        print(f"Error in chapter planning: {e}")
        return

if __name__ == "__main__":
    run_book_planning(
        model_path="design/samples/book_model.json",
        blueprint_path="design/samples/blueprint.json",
        research_path="design/samples/research-result.json",
        planning_txt_path="design/samples/plan.md",
        summary_txt_path="design/samples/summary-response.md",
        out_path="design/samples/book_plan.json"
    )
    # run_chapter_planning(
    #     research_path="design/samples/research-result.json",
    #     book_plan_path="design/samples/book_plan.json",
    #     summary_path="design/samples/summary-response.md",
    #     out_path="design/samples/"
    # )
