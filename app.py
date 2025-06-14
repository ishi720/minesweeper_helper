from flask import Flask, render_template_string
import itertools
import numpy as np

app = Flask(__name__)

initial_grid = np.array([
    [0, 4, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0]
])
GRID_SIZE = 5
NUM_ITEMS = 10
empty_positions = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if initial_grid[r][c] == 0]

def calculate_visibility(grid, row, col):
    count = 0
    for i in range(row - 1, -1, -1):
        if grid[i][col] == 'x':
            break
        count += 1
    for i in range(row + 1, GRID_SIZE):
        if grid[i][col] == 'x':
            break
        count += 1
    for j in range(col - 1, -1, -1):
        if grid[row][j] == 'x':
            break
        count += 1
    for j in range(col + 1, GRID_SIZE):
        if grid[row][j] == 'x':
            break
        count += 1
    return count

def is_valid_pattern(grid, initial_grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if initial_grid[row][col] > 0:
                if calculate_visibility(grid, row, col) != initial_grid[row][col]:
                    return False
    return True

@app.route('/')
def index():
    all_combinations = itertools.combinations(empty_positions, NUM_ITEMS)
    valid_patterns = []

    max_display = 5
    count = 0

    for comb in all_combinations:
        grid = initial_grid.copy().astype(str)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if grid[r][c] == '0':
                    grid[r][c] = '.'
        for r, c in comb:
            grid[r][c] = 'x'
        if is_valid_pattern(grid, initial_grid):
            valid_patterns.append(grid)
            count += 1
            if count >= max_display:
                break

    html = '''
    <h1>Valid Patterns (up to {{max}})</h1>
    {% for pattern in patterns %}
    <table border="1" style="border-collapse: collapse; margin-bottom: 20px;">
        {% for row in pattern %}
        <tr>
            {% for cell in row %}
            <td style="width: 20px; height: 20px; text-align: center;">{{ cell }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No valid pattern found.</p>
    {% endfor %}
    '''
    return render_template_string(html, patterns=valid_patterns, max=max_display)

if __name__ == '__main__':
    app.run(debug=True)