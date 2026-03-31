# ============================================
# 🔄 AUTO-UPDATE SCRIPT
# ============================================
# This script automatically:
# 1. Pulls latest code from GitHub
# 2. Reloads all Python modules
# 3. Preserves your running variables
#
# Just run this cell whenever you encounter an error!
# ============================================

import subprocess
import importlib
import sys
from pathlib import Path
import os

def auto_update_and_reload():
    """
    Automatically pull latest code and reload modules
    """
    print("🔄 AUTO-UPDATE STARTING...\n")
    print("=" * 60)

    # Step 1: Get repository root
    try:
        notebook_dir = Path.cwd()
        if notebook_dir.name == 'notebooks':
            repo_root = notebook_dir.parent
        else:
            repo_root = notebook_dir

        print(f"📁 Repository: {repo_root}")

        # Step 2: Stash any local changes
        print("\n💾 Saving local changes...")
        stash_result = subprocess.run(
            ["git", "stash"],
            cwd=str(repo_root),
            capture_output=True,
            text=True
        )

        if "No local changes to save" in stash_result.stdout:
            print("   ✅ No local changes to stash")
        else:
            print("   ✅ Local changes stashed")

        # Step 3: Pull latest code
        print("\n⬇️ Pulling latest code from GitHub...")
        pull_result = subprocess.run(
            ["git", "pull", "origin", "claude/rebuild-proposal-builder-011CUXXm3yt3mm1e8cP6UcMb"],
            cwd=str(repo_root),
            capture_output=True,
            text=True
        )

        if "Already up to date" in pull_result.stdout:
            print("   ✅ Already up to date")
        elif pull_result.returncode == 0:
            print("   ✅ Successfully pulled updates")
            print(f"   Changes: {pull_result.stdout.strip()}")
        else:
            print(f"   ⚠️ Pull had issues: {pull_result.stderr}")

        # Step 4: Reload all custom modules
        print("\n🔥 Hot-reloading Python modules...")

        modules_to_reload = [
            'data_models',
            'rag_engine',
            'agents',
            'utils',
            'visualizations',
            'exports'
        ]

        reloaded_count = 0
        for module_name in modules_to_reload:
            if module_name in sys.modules:
                try:
                    importlib.reload(sys.modules[module_name])
                    print(f"   ✅ {module_name}")
                    reloaded_count += 1
                except Exception as e:
                    print(f"   ⚠️ {module_name}: {e}")
            else:
                print(f"   ⏭️ {module_name} (not loaded)")

        print(f"\n✅ Reloaded {reloaded_count} module(s)")

        # Step 5: Re-import key classes
        print("\n📦 Re-importing classes...")

        try:
            from data_models import ProjectStructure, Workstream, Module, Activity
            from rag_engine import RAGEngine
            from agents import WorkstreamAgent, DependencyAgent, ModuleAgent, TimelineOptimizer
            from utils import validate_environment, save_project, load_project, list_saved_projects
            from visualizations import ProjectVisualizer
            from exports import export_project

            print("   ✅ All classes imported successfully!")

        except Exception as e:
            print(f"   ⚠️ Import error: {e}")

        # Step 6: Verify variables are preserved
        print("\n🔍 Checking preserved variables...")

        preserved_vars = []
        check_vars = ['rag_engine', 'project', 'rfp_text', 'enhanced_workstreams', 'viz']

        for var_name in check_vars:
            if var_name in globals():
                preserved_vars.append(var_name)
                print(f"   ✅ {var_name} is still available")

        if not preserved_vars:
            print("   ℹ️ No variables to preserve (fresh start)")

        print("\n" + "=" * 60)
        print("🎉 AUTO-UPDATE COMPLETE!")
        print("=" * 60)
        print("\n💡 Next: Re-run the cell that had an error")

    except Exception as e:
        print(f"\n❌ Error during auto-update: {e}")
        import traceback
        traceback.print_exc()

# Run the auto-update
auto_update_and_reload()
