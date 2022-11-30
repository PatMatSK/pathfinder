import tkinter as tk
root = tk.Tk()
root.title("Path Finder")
widthCan = 1000
heightCan = 550
size = 10
canvas = tk.Canvas(root, width=widthCan, height=heightCan)
lines = []


def get_data(file: str = ""):
    try:
        data = open(file, encoding="utf-8")
    except FileNotFoundError:
        print("File not found")
        return {}

    graph = {}
    for i in data:
        town = i.split(";")[0]
        graph[town] = (int(i.split(";")[1]), int(i.split(";")[2]))
    return graph


def show_towns(towns_coords):
    if towns_coords is None:
        return

    for coord in towns_coords:
        x = int(towns_coords[coord][0])
        y = int(towns_coords[coord][1])
        canvas.create_oval(x - (size // 2), y - (size // 2), x + (size // 2), y + (size // 2), fill="blue")
        canvas.create_text(x, y + size, text=coord)


def get_distance(_from, _to, town_coords):
    a = town_coords[_from]
    b = town_coords[_to]
    return round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5, 1)  # pytagoras


def add_to_graph(_from, _to, graph, towns_coords):
    dist = get_distance(_from, _to, towns_coords)
    if _from not in graph:
        graph[_from] = {_to: dist}
    else:
        if _to not in graph[_from]:
            graph[_from][_to] = dist

# {'Bratislava': ['Dunajská Streda', 'Senec', 'Malacky'], 'Dunajská Streda': ['Brati


def create_graph(towns_coords, edges_file):
    """ create main graph and print edges """
    try:
        file = open(edges_file, encoding="utf-8")
    except FileNotFoundError:
        print("File not found")
        return

    graph = {}
    for line in file:
        a_town = line.split(";")[0].strip()
        b_town = line.split(";")[1].strip()

        add_to_graph(a_town, b_town, graph, towns_coords)
        add_to_graph(b_town, a_town, graph, towns_coords)

        first = towns_coords[a_town]
        second = towns_coords[b_town]
        canvas.create_line(first[0], first[1], second[0], second[1])

    return graph



def clear_lines():
    global lines
    for line in lines:
        canvas.delete(line)


def build_path(finish, visited, towns_coords):
    target = finish
    while visited[target][0] != '':
        previous = visited[target][0]
        x0 = towns_coords[previous][0]
        y0 = towns_coords[previous][1]
        x1 = towns_coords[target][0]
        y1 = towns_coords[target][1]
        lines.append(canvas.create_line(x0, y0, x1, y1, width=5))
        target = previous


def find_path(start, finish, graph, towns_coords):
    """ searches for shortest path from start to finish with BFS"""
    clear_lines()
    if start not in towns or finish not in towns:
        return

    to_visit = [start]

    visited = {start: ['', 0]}          # {'to':('from', distance) }
    flag = False
    while to_visit:
        current = to_visit[0]
        for neighbor in graph[current]:
            new_dist = visited[current][1] + graph[current][neighbor]
            if neighbor in visited and visited[neighbor][1] < new_dist:
                continue
            visited[neighbor] = [current, new_dist]
            to_visit.append(neighbor)
            if neighbor == finish:
                flag = True
                break
        if flag:
            break
        to_visit.pop(0)

    build_path(finish, visited, towns_coords)


towns_coords = get_data("towns.txt")
show_towns(towns_coords)
graph = create_graph(towns_coords, "edges.txt")
towns = towns_coords.keys()

start_label = tk.Label(root, text="Start:")
finish_label = tk.Label(root, text="Finish:")
start_entry = tk.Entry(root, bg="lightblue")
finish_entry = tk.Entry(root, bg="lightblue")
button = tk.Button(root, text="Find Path", command=lambda: find_path(start_entry.get(), finish_entry.get(),
                                                                     graph, towns_coords))

canvas.pack()
start_label.pack(side="left")
start_entry.pack(side="left")
finish_label.pack(side="left")
finish_entry.pack(side="left")
button.pack(side="left")

root.bind('<Return>', lambda event: find_path(start_entry.get(), finish_entry.get(), graph, towns_coords))

root.mainloop()
