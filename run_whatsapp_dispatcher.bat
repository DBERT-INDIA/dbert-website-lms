@echo off
cd /d "%~dp0"

:MENU
cls
echo ========================================================================
echo        DBERT CANDIDATE WHATSAPP DISPATCHER (DUAL ACCOUNT ENGINE)
echo ========================================================================
echo   Target Campaign : 409 Provisional Certificate Recipients
echo   Batch Strategy  : 92 Candidates per Batch (46 per Account)
echo   Pacing Schedule : Continuous 18s-35s randomized human breaks
echo   Registry Source : data\all_409_provisional_registry.json
echo   Portal Domain   : https://dbert.in/verify
echo ========================================================================
echo.
echo   [V] PRE-FLIGHT VERIFIER AND LAUNCH   : Check Sessions, Scan QR and Auto-Start
echo   [1] LAUNCH DUAL WORKERS (PARALLEL)   : Start Sending Current Queue
echo   [2] LOAD NEXT BATCH OF REMAINING     : Queue Next 92 Remaining (Latest Signups First)
echo   [3] LOAD NEXT BATCH AND LAUNCH       : One-Click Load Remaining and Start Both
echo   [4] PREVIEW CURRENT QUEUE (Dry Run)  : Inspect 46+46 Split and Sample Message
echo   [5] PROGRESS AND CAMPAIGN STATUS     : See Total Sent vs Remaining Pool
echo   [6] SEND TEST MESSAGE                : Send 1 Sample Message to Your Own Phone
echo   [7] RUN ACCOUNT 1 ONLY (ODD)         : Dispatch 46 Candidates from Account 1
echo   [8] RUN ACCOUNT 2 ONLY (EVEN)        : Dispatch 46 Candidates from Account 2
echo   [9] RESET FAILED TO PENDING          : Retry Failed Deliveries
echo   [L1] LOGIN / SCAN QR FOR ACCOUNT 1   : Open Chrome and Scan QR for Account 1
echo   [L2] LOGIN / SCAN QR FOR ACCOUNT 2   : Open Chrome and Scan QR for Account 2
echo   [C] SYNC EMAIL AND WHATSAPP (Report) : Cross-Reference with Email Records
echo   [0] EXIT
echo.
echo ========================================================================
set choice=
set /p choice=Enter your choice (0-9, V, L1, L2, or C): 

if /i "%choice%"=="V" goto OPTIONV
if /i "%choice%"=="L1" goto OPTIONL1
if /i "%choice%"=="L2" goto OPTIONL2
if /i "%choice%"=="C" goto OPTIONC
if "%choice%"=="1" goto OPTION1
if "%choice%"=="2" goto OPTION2
if "%choice%"=="3" goto OPTION3
if "%choice%"=="4" goto OPTION4
if "%choice%"=="5" goto OPTION5
if "%choice%"=="6" goto OPTION6
if "%choice%"=="7" goto OPTION7
if "%choice%"=="8" goto OPTION8
if "%choice%"=="9" goto OPTION9
if "%choice%"=="0" goto OPTION0

echo.
echo Invalid choice "%choice%". Please select from the menu.
echo.
pause
goto MENU

:OPTIONV
cls
echo ========================================================================
echo   [PRE-FLIGHT] Verifying Sessions, QR Codes and Parallel Launch
echo ========================================================================
python scripts\verify_and_launch_dbert_whatsapp.py
echo.
pause
goto MENU

:OPTIONL1
cls
call "%~dp0login_acc1.bat"
goto MENU

:OPTIONL2
cls
call "%~dp0login_acc2.bat"
goto MENU

:OPTION1
cls
echo ========================================================================
echo   [ACTION] Launching Account 1 and Account 2 in parallel windows...
echo ========================================================================
start "DBERT Account 1 (Odd - Green)" "%~dp0run_worker_acc1.bat"
start "DBERT Account 2 (Even - Yellow)" "%~dp0run_worker_acc2.bat"
echo.
echo   [OK] Both worker windows have been started!
echo   - Window 1 (Green) : Account 1 (46 Odd candidates)
echo   - Window 2 (Yellow): Account 2 (46 Even candidates)
echo.
pause
goto MENU

:OPTION2
cls
echo ========================================================================
echo   [ACTION] Loading Next Batch of Remaining Candidates...
echo ========================================================================
python scripts\send_dbert_whatsapp.py --next-batch
echo.
echo ========================================================================
echo   Batch loaded successfully! (46 for Account 1, 46 for Account 2)
echo   Do you want to start sending messages now?
echo   - Type [1] or [Y] and press Enter to LAUNCH DUAL WORKERS NOW
echo   - Type [V] and press Enter to VERIFY SESSIONS AND AUTO-START
echo   - Press [Enter] to return to Main Menu
echo ========================================================================
set launch_now=
set /p launch_now=Enter choice (1/Y to Send, V to Verify, Enter for Menu): 
if /i "%launch_now%"=="1" goto OPTION1
if /i "%launch_now%"=="Y" goto OPTION1
if /i "%launch_now%"=="V" goto OPTIONV
goto MENU

:OPTION3
cls
echo ========================================================================
echo   [ACTION] Loading Next Batch and Launching Dual Workers...
echo ========================================================================
python scripts\send_dbert_whatsapp.py --next-batch
echo.
echo   [ACTION] Starting Account 1 and Account 2 workers in parallel...
start "DBERT Account 1 (Odd - Green)" "%~dp0run_worker_acc1.bat"
start "DBERT Account 2 (Even - Yellow)" "%~dp0run_worker_acc2.bat"
echo.
echo   [OK] Both worker windows have been started!
echo   - Window 1 (Green) : Account 1 (46 Odd candidates)
echo   - Window 2 (Yellow): Account 2 (46 Even candidates)
echo.
pause
goto MENU

:OPTION4
cls
python scripts\send_dbert_whatsapp.py --dry-run
echo.
echo ========================================================================
echo   Ready to send these 92 messages across Account 1 and Account 2?
echo   - Type [1] or [Y] and press Enter to LAUNCH DUAL WORKERS NOW
echo   - Type [V] and press Enter to VERIFY SESSIONS AND AUTO-START
echo   - Press [Enter] to return to the main menu
echo ========================================================================
set send_now=
set /p send_now=Enter choice (1/Y to Send, V to Verify, Enter for Menu): 
if /i "%send_now%"=="1" goto OPTION1
if /i "%send_now%"=="Y" goto OPTION1
if /i "%send_now%"=="V" goto OPTIONV
goto MENU

:OPTION5
cls
python scripts\send_dbert_whatsapp.py --status
echo.
pause
goto MENU

:OPTION6
cls
echo ========================================================================
echo   [TEST] Send Sample Message to Your Own Phone
echo ========================================================================
echo Enter target phone number with 91 country code (e.g. 919876543210):
set testphone=
set /p testphone=Phone number: 
if "%testphone%"=="" goto MENU
echo Which account to test from? [1] Account 1 (Odd), [2] Account 2 (Even):
set testacc=1
set /p testacc=Account (1 or 2, default 1): 
python scripts\send_dbert_whatsapp.py --test-to %testphone% --account %testacc%
echo.
pause
goto MENU

:OPTION7
cls
call "%~dp0run_worker_acc1.bat"
goto MENU

:OPTION8
cls
call "%~dp0run_worker_acc2.bat"
goto MENU

:OPTION9
cls
echo [ACTION] Resetting FAILED candidates back to PENDING...
python scripts\send_dbert_whatsapp.py --reset-failed
echo.
pause
goto MENU

:OPTIONC
cls
echo ========================================================================
echo   CROSS-REFERENCING EMAIL AND WHATSAPP TRACKING STATE
echo ========================================================================
python scripts\send_dbert_whatsapp.py --sync-email
echo.
pause
goto MENU

:OPTION0
echo Exiting DBERT WhatsApp Dispatcher.
exit /b 0
