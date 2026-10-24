with open('apps/portal/app.py', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if '_POSTS_PER_PAGE' in line and '=' in line and 'POSTS_PER_PAGE =' in line:
            print(i, line.rstrip())
            break
