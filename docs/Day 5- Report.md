# Day 5 Report – Matching Accuracy & Proposal Quality Improvements

**Date:** 07 August 2026

## Overview
Focused on improving the quality of company matching and proposal generation by replacing unreliable LLM-based scoring with deterministic matching logic. Planned enhancements to company extraction, technology detection, and crawl filtering were also documented.

## Tasks Completed

### 1. Improved Candidate Matching Strategy

- Reviewed the existing matching pipeline.
- Identified that LLM-generated match scores were inconsistent.
- Planned deterministic score calculation using company technologies and candidate skills.
- Decided to use set intersection for accurate skill matching.

### 2. Matching Agent Enhancement Plan

- Planned technology normalization before comparison.
- Designed automatic matched and missing skill detection.
- Moved score calculation from the LLM to application logic.
- Reserved the LLM only for generating reasoning and recommendations.

### 3. Company Extraction Improvements

- Identified incorrect company extraction from article pages.
- Planned prompt updates to ensure the website owner is extracted instead of companies mentioned within articles.
- Added examples to improve extraction reliability.

### 4. Crawl Filtering Improvements

- Planned blacklist filtering for blogs, rankings, startup lists, and comparison pages.
- Designed page title validation to reject "Top Companies", "Best", "Ranking", and similar pages before extraction.
- Reduced unnecessary crawling of irrelevant pages.

### 5. Technology Extraction Enhancement

- Expanded extraction requirements for technologies.
- Planned extraction of:
  - Programming languages
  - AI frameworks
  - ML libraries
  - Cloud platforms
  - Deployment technologies
  - Development frameworks

### 6. Proposal Generation Improvement

- Updated proposal generation strategy.
- Planned proposal generation when:
  - Match score ≥ 60, or
  - At least three skills match.
- Reduced unnecessary rejection of suitable companies.

## Files Updated

- `app/agents/matching_agent.py`
- `app/prompts/matching_prompt.py`
- `app/prompts/extraction_prompt.py`
- `app/crawler/scraper.py`
- `app/main.py`
