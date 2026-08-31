import os
import subprocess
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Change this to the absolute path of your local GitHub repo folder
load_dotenv()
REPO_PATH = os.getenv("REPO_PATH") 

def index(request):
    return render(request, 'editor/index.html')

@csrf_exempt
def execute_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        rating = str(data.get('rating', '800'))
        contest = str(data.get('contest', '0000'))
        problem = str(data.get('problem', 'A'))
        test_input = data.get('input', '')

        # 1. Create Directory Structure: repo/rating/contest/problem/
        dir_path = os.path.join(REPO_PATH, rating, contest, problem)
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, 'main.cpp')
        executable_path = os.path.join(dir_path, 'main')

        # 2. Save the code
        with open(file_path, 'w') as f:
            f.write(code)

        # 3. Compile the code
        compile_process = subprocess.run(
            ['g++', file_path, '-o', executable_path],
            capture_output=True, text=True
        )

        if compile_process.returncode != 0:
            return JsonResponse({'status': 'error', 'output': compile_process.stderr})

        # 4. Run the code with custom input
        try:
            run_process = subprocess.run(
                [executable_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=3 # Prevent infinite loops
            )
            return JsonResponse({
                'status': 'success', 
                'output': run_process.stdout,
                'error': run_process.stderr
            })
        except subprocess.TimeoutExpired:
            return JsonResponse({'status': 'error', 'output': 'Time Limit Exceeded (3s)'})

@csrf_exempt
def push_to_github(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = str(data.get('rating', '800'))
        contest = str(data.get('contest', '0000'))
        problem = str(data.get('problem', 'A'))

        commit_message = f"Solved {contest}{problem} (Rating: {rating})"

        try:
            # Run git commands sequentially in the repo directory
            subprocess.run(['git', 'add', '.'], cwd=REPO_PATH, check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=REPO_PATH, check=True)
            subprocess.run(['git', 'push'], cwd=REPO_PATH, check=True)
            
            return JsonResponse({'status': 'success', 'message': 'Successfully pushed to GitHub!'})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})