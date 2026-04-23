import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, master):
        self.master = master
        master.title("Личная кинотека")
        self.data_file = "movies.json"
        self.movies = []

        # Поля ввода
        self.frame_input = tk.Frame(master)
        self.frame_input.pack(pady=10)

        tk.Label(self.frame_input, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_title = tk.Entry(self.frame_input, width=20)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_input, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_genre = tk.Entry(self.frame_input, width=20)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.frame_input, text="Год выпуска:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_year = tk.Entry(self.frame_input, width=10)
        self.entry_year.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_input, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.entry_rating = tk.Entry(self.frame_input, width=10)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка для добавления фильма
        self.btn_add = tk.Button(master, text="Добавить фильм", command=self.add_movie)
        self.btn_add.pack(pady=5)

        # Фильтры
        self.frame_filters = tk.Frame(master)
        self.frame_filters.pack(pady=10)

        tk.Label(self.frame_filters, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.combo_genre_filter = ttk.Combobox(self.frame_filters, values=[], state='readonly')
        self.combo_genre_filter.grid(row=0, column=1, padx=5)
        self.combo_genre_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(self.frame_filters, text="Фильтр по году:").grid(row=0, column=2, padx=5)
        self.combo_year_filter = ttk.Combobox(self.frame_filters, values=[], state='readonly')
        self.combo_year_filter.grid(row=0, column=3, padx=5)
        self.combo_year_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        # Таблица (Treeview)
        self.tree = ttk.Treeview(master, columns=("Название", "Жанр", "Год", "Рейтинг"), show='headings', height=10)
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.pack(pady=10)

        # Загрузка данных
        self.load_data()
        self.update_filters()

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        # Проверки
        if not title or not genre or not year or not rating:
            messagebox.showwarning("Внимание", "Заполните все поля")
            return
        if not year.isdigit():
            messagebox.showwarning("Внимание", "Год должен быть числом")
            return
        try:
            rating_value = float(rating)
            if not (0 <= rating_value <= 10):
                raise ValueError
        except:
            messagebox.showwarning("Внимание", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": rating_value
        }
        self.movies.append(movie)
        self.save_data()
        self.refresh_table()
        self.update_filters()
        self.clear_fields()

    def clear_fields(self):
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.movies = json.load(f)
        else:
            self.movies = []
        self.refresh_table()

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def refresh_table(self, filtered_movies=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data_to_show = filtered_movies if filtered_movies is not None else self.movies
        for m in data_to_show:
            self.tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

    def update_filters(self):
        genres = sorted(set(m['genre'] for m in self.movies))
        years = sorted(set(str(m['year']) for m in self.movies))
        self.combo_genre_filter['values'] = ['Все'] + genres
        self.combo_year_filter['values'] = ['Все'] + years
        self.combo_genre_filter.set('Все')
        self.combo_year_filter.set('Все')

    def apply_filters(self, event=None):
        genre_filter = self.combo_genre_filter.get()
        year_filter = self.combo_year_filter.get()
        filtered = self.movies

        if genre_filter != 'Все':
            filtered = [m for m in filtered if m['genre'] == genre_filter]
        if year_filter != 'Все':
            filtered = [m for m in filtered if str(m['year']) == year_filter]

        self.refresh_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
