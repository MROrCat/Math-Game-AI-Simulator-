'''Strat13. На доске записано целое положительное число N. Два игрока ходят по очереди. За ход
разрешается либо заменить число на доске на один из его делителей (отличных от единицы и
самого числа), либо уменьшить число на единицу (если при этом число остается
положительным). Тот, кто не может сделать ход, проигрывает.'''

import math

class Game:
    """Класс Game хранит состояние игры и отвечает за правила."""
    def __init__(self, n):
        self.current_number = n

    def get_valid_moves(self, n=None):
        """Возвращает список доступных чисел для хода."""
        if n is None:
            n = self.current_number
        if n <= 1:
            return []
        
        # Правило 2: уменьшить число на единицу
        moves = [n - 1]
        
        # Правило 1: заменить на один из собственных делителей
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                moves.append(i)
                if i * i != n:
                    moves.append(n // i)
                    
        return sorted(list(set(moves)))

    def make_move(self, move):
        """Обновляет текущее число на доске."""
        self.current_number = move

    def is_game_over(self):
        """Проверяет, завершена ли игра."""
        return len(self.get_valid_moves()) == 0


class Player:
    """Базовый класс игрока."""
    def __init__(self, name):
        self.name = name

    def choose_move(self, game):
        raise NotImplementedError


class HumanPlayer(Player):
    """Класс игрока-человека с вводом из консоли."""
    def choose_move(self, game):
        valid_moves = game.get_valid_moves()
        print(f"Доступные числа для хода: {valid_moves}")
        while True:
            try:
                move = int(input(f"{self.name}, выберите число из списка: "))
                if move in valid_moves:
                    return move
                print("Ошибка! Данное число недоступно для хода.")
            except ValueError:
                print("Пожалуйста, введите корректное целое число.")


class AIPlayer(Player):
    """Класс компьютерного противника с алгоритмом Minimax."""
    def __init__(self, name):
        super().__init__(name)
        self.memo = {}

    def minimax(self, n, game):
        """Анализирует позицию методом мемоизации."""
        if n <= 1:
            return False  # Проигрышная позиция (нет ходов)
        if n in self.memo:
            return self.memo[n]
        
        # Если хотя бы один доступный ход ведет к проигрышу соперника, 
        # то текущая позиция является выигрышной.
        for move in game.get_valid_moves(n):
            if not self.minimax(move, game):
                self.memo[n] = True
                return True
                
        self.memo[n] = False
        return False

    def choose_move(self, game):
        valid_moves = game.get_valid_moves()
        
        # Ищем идеальный ход, который гарантирует победу
        for move in valid_moves:
            if not self.minimax(move, game):
                print(f" {self.name} делает идеальный ход: {move}")
                return move
                
        # Если идеального хода нет, ходим на первое доступное число
        print(f" {self.name} делает вынужденный ход: {valid_moves[0]}")
        return valid_moves[0]


def main():
    print("=== Старт игры Strat13 ===")
    while True:
        try:
            n = int(input("Введите начальное положительное число N (больше 1): "))
            if n > 1:
                break
            print("Число должно быть строго больше 1.")
        except ValueError:
            print("Введите целое число.")
            
    game = Game(n)
    player1 = HumanPlayer("Игрок (Вы)")
    player2 = AIPlayer("Компьютер (ИИ)")
    
    players = [player1, player2]
    turn_index = 0
    
    # Главный игровой цикл
    while not game.is_game_over():
        print(f"\nЧисло на доске: {game.current_number}")
        current_player = players[turn_index]
        
        move = current_player.choose_move(game)
        game.make_move(move)
        
        if game.is_game_over():
            print(f"\nНа доске осталось число {game.current_number}. Ходов больше нет.")
            print(f"🎉 Победил {current_player.name}!")
            break
            
        turn_index = 1 - turn_index


if __name__ == "__main__":
    main()
