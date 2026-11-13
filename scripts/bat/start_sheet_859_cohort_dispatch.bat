@echo off
title DBERT Sheet 859 Cohort Application Batch Dispatcher
echo ======================================================================
echo Starting Live Multi-Account Dispatch for Sheet 859 (840 Unique Candidates)
echo ======================================================================
cd /d "%~dp0\..\.."
python scripts\dispatch_sheet_859_cohort.py --live
pause
