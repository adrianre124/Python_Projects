import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Wartości czy pole jest aktywne czy nie
ON = 1
OFF = 0
vals = [ON, OFF]

# Stworzenie planszy
grid_size = (100, 100)
grid = np.zeros(grid_size, dtype=int)

# Wylosowanie zapełnienia planszy
def initial_grid():
    initial_state = np.random.choice(vals, size=grid_size, p=[0.2, 0.8])
    grid[:initial_state.shape[0], :initial_state.shape[1]] = initial_state

# Kolejna iteracja
def update():
    new_grid = grid.copy()
    
    # Przejście przez wszyskie komórki na planszy
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            cell = grid[i, j]
            # Zliczanie ilości aktywnych sąsiednich komórek
            neighbors = grid[i-1:i+2, j-1:j+2]
            total = np.sum(neighbors) - cell

            # Zasady Game Of Life
            if cell == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON
    
    # Zmiana stanu planszy
    grid[:] = new_grid

# Zapisywanie planszy do pliku
def save_to_file(filename, iteration):
    with open(filename, 'a') as f:
        grid_str = ''.join(map(str, grid.flatten().tolist()))
        f.write(f"{iteration}, {grid_str}\n")

# Przejście do następnej iteracji po kliknięciu
def next_iteration(event):
    global iteration
    iteration += 1
    update()
    plt.clf()
    show_figure(iteration)
    save_to_file('game_of_life.txt', iteration)

# Wyświetlenie planszy
def show_figure(iteration):
    plt.imshow(grid)
    plt.title(f'Iteration: {iteration}')

    # Przycisk do przechodzenia do następnej iteracji
    ax_next = plt.axes([0.7, 0.01, 0.1, 0.04])
    btn_next = Button(ax_next, "Next")
    btn_next.on_clicked(next_iteration)

    plt.show()
    plt.pause(0.001)

def main():
    initial_grid()

    show_figure(iteration)
    save_to_file('game_of_life.txt', iteration)

if __name__ == '__main__':
    iteration = 0

    main()

# 4. Napisz program "Conway's Game of Life" (https://playgameoflife.com/info).  
# Założenia:
#   - wielkość mapy: (100, 100)  
#   - komórki pojawiają się względem punktu (50, 50)  
#   - komórki, które wychodzą poza obszar umierają  
# Kryteria akceptacji:  
#   - wizualizacja, z możliwą zmianą czasu wyświetlania pojedyńczego "dnia życia" komórek  
#   - funkcją, która generuje różne rozmieszczenia komórek i uruchamia symulację  
#   - czas życia kolonii oraz ustawienie początkowe są zapisywane w pliku, gdzie każda iteracja symulacji j jest kolejnym wierszem, a ustawienie początkowe i czas życia kolonii kolumnami  
#   - zawierać interfejs graficzny (z użyciem matplotlib) 