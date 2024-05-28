from pathlib import Path
current_dir = Path(__file__).parent
env_dir = current_dir.parents[1]

file_name = env_dir / '.env'
k=''
with open(file_name, 'r') as f:
    k=f.read()

print(k)



