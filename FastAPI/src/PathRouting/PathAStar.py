import heapq


class AStarSearch:
    def __init__(self, graph, start, end, custom_cost):
        self.graph = graph
        self.start = start
        self.end = end
        self.heuristic_cost = self.heuristic
        self.custom_cost = custom_cost

    def heuristic(self, a, b):
        (x1, y1) = self.graph.nodes[a]['y'], self.graph.nodes[a]['x']
        (x2, y2) = self.graph.nodes[b]['y'], self.graph.nodes[b]['x']
        # Calculate the custom heuristic cost based on Euclidean distance
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def a_star_search(self):
        frontier = []
        heapq.heappush(frontier, (0, self.start))
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == self.end:
                break

            neighbors = self.graph.neighbors(current_node)
            for neighbor in neighbors:
                new_cost = cost_so_far[current_node] + self.custom_cost(current_node, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic_cost(neighbor, self.end)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current_node

        path = self.reconstruct_path(came_from, self.start, self.end)
        return path

    def reconstruct_path(self, came_from, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
