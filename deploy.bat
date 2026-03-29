@echo off
echo =======================================
echo Odesilam nova data na Vercel...
echo =======================================
git add .
git commit -m "Auto-deploy: CRM Data Pipeline Update"
git push
echo.
echo [USPECH] Odeslano! Vercel prave stavi novou verzi webu.