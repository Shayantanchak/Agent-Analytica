import subprocess
import sys
import os

def main():
    print("=============================================")
    print(" 🚀 Initializing Analytica Agentic Engine...")
    print("=============================================\n")
    
    app_path = os.path.join(os.path.dirname(__file__), "app", "ui_streamlit.py")
    
    if not os.path.exists(app_path):
        print(f"❌ Error: Could not find the core application dashboard at {app_path}")
        sys.exit(1)
        
    try:
        # Executes the Streamlit server directly from the native Python environment
        print("Starting local execution server... (Press CTRL+C to sequence shutdown)\n")
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
        
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt detected. Turning off Analytica Agentic Engine gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
