import os
import subprocess
import shutil

def launch_power_bi():
    # 1. Check for Microsoft Store version (AppID)
    store_app_id = "Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe!Microsoft.MicrosoftPowerBIDesktop"
    
    # 2. Check for Standalone Standard paths
    standalone_paths = [
        r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
        r"C:\Program Files (x86)\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
    ]

    print(f"🚀 Searching for Power BI Desktop...")

    # Try Standalone first (often preferred for custom setups)
    for path in standalone_paths:
        if os.path.exists(path):
            print(f"✅ Found Standalone version at: {path}")
            try:
                subprocess.Popen([path])
                print("✨ Power BI (Standalone) has been launched.")
                return
            except Exception as e:
                print(f"⚠️ Error launching Standalone version: {e}")

    # Try Store version via explorer.exe
    print(f"🔍 Standalone not found. Trying Store version...")
    try:
        # We use Popen instead of run to not block the script
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{store_app_id}"])
        print("✅ Power BI (Store) launch request sent.")
    except Exception as e:
        print(f"❌ Error launching Power BI Store version: {e}")
        print("\n💡 Tip: If Power BI is not installed, download it here:")
        print("🔗 https://powerbi.microsoft.com/desktop/")

if __name__ == "__main__":
    launch_power_bi()

