import os

from tkinter import *
import tkinter.messagebox
import imdb
import json

class MovieRatings(Frame):
    """Our main window."""

    def __init__(self, parent):
        """Initialization of class variables."""
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Филми")
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_columnconfigure(1, weight=0)
        self.movies_db = imdb.IMDb()
        self.movies_dict = {}
        self.filename = 'movies.json'

        self.initUI()

    def initUI(self):
        """Initialization of user interface."""
        self.label_name = Label(text='Име на филм: ')
        self.label_name.grid(row=1, column=0, sticky=W, padx=2, pady=2, rowspan=1, columnspan = 1)
        self.input_name = Entry(self.parent, width=35, borderwidth=5)
        self.input_name.grid(row=2, column=0, sticky=W, padx=2, pady=2, rowspan=1, columnspan = 2)

        self.label_score = Label(text='Оценка на филм: ')
        self.label_score.grid(row=3, column=0, sticky=W, padx=2, pady=2, rowspan=1, columnspan = 1)
        self.input_score = Entry(self.parent, width=35, borderwidth=5)
        self.input_score.grid(row=4, column=0, sticky=W, padx=2, pady=2, rowspan=1, columnspan = 2)

        self.load_DB_file()

        self.listbox_movies = Listbox(self.parent, height=10, width=25, borderwidth=5, selectmode=SINGLE)
        self.listbox_movies.grid(row=2, column=1, padx=2, pady=2, rowspan=5, columnspan = 5)

        for key, value in self.movies_dict.items():
            self.listbox_movies.insert(END, '{}: {}'.format(key, self.movies_dict[key]))

        self.movie_info_IMDb = Label(text='IMDB Ratings:')
        self.movie_info_IMDb.grid(row=5, column=0, sticky=W)

        btn_add = Button(self.parent, text="Добави", command=self.button_add)
        btn_add.grid(row=0, column=0, padx=0, pady=1)

        btn_get_ratings = Button(self.parent, text="Вземи райтинг", command=self.button_get_rating)
        btn_get_ratings.grid(row=0, column=1, padx=0, pady=1)

        btn_remove = Button(self.parent, text="Премахни филма",
                            command=lambda listbox=self.listbox_movies: [self.button_delete(listbox), listbox.delete(ANCHOR)])
        btn_remove.grid(row=0, column=2, padx=0, pady=1)

        btn_save = Button(self.parent, text="Запази филмите",
                          command = lambda : self.button_save())
        btn_save.grid(row=0, column=3, padx=1, pady=1)

        btn_exit = Button(self.parent, text="Излез",
                          command = lambda : self.parent.destroy())
        btn_exit.grid(row=0, column=4, padx=1, pady=1)

    def load_DB_file(self):
        """Loading of the stored JSON data base file."""
        if os.path.isfile(self.filename) and os.access(self.filename, os.R_OK):
            with open(self.filename, 'a+') as movies_file:
                movies_file.seek(0)
                self.movies_dict = json.load(movies_file)
                movies_file.close()
        else:
            self.movies_dict = {}

    def button_save(self):
        """Saving of the JSON data base file.."""
        with open(self.filename, 'w') as movies_file:
            movies_file.write(json.dumps(self.movies_dict))

        movies_file.close()
        tkinter.messagebox.showinfo('FYI', 'File Saved.')

    def button_add(self):
        """Adding movie to our list of movies."""
        current_name = self.input_name.get()
        current_score = self.input_score.get()
        self.movies_dict.update({current_name: current_score})

        self.listbox_movies.insert(END, current_name + ' - ' + current_score + '\n')

        # [TODO]: This is just for test, needs to go when app is finished!
        print(self.movies_dict)

        self.input_name.delete(0, END)
        self.input_score.delete(0, END)

    def button_get_rating(self):
        """Getting the IMDB movie ratings."""
        selection = self.listbox_movies.curselection()
        if selection:
            selected_movie = self.listbox_movies.get(ANCHOR)
            selected_movie = self.movies_db.search_movie(selected_movie)
            # If the movie is found then get the ID and the rating.
            if selected_movie:
                id = selected_movie[0].getID()
                movie = self.movies_db.get_movie(id)
                rating = movie['rating']
                # [TODO]: For testing only, remove when done.
                print(rating)
                if rating:
                    self.movie_info_IMDb.configure(text='IMDB ratings: ' + str(rating))
                else:
                    self.movie_info_IMDb.configure(text="No IMDB ratings found!")
            else: # If the movie is not found give a message.
                self.movie_info_IMDb.configure(text="No IMDB ratings found!")

    def button_delete(self, listbox):
        """Delete the selected movie."""
        selected_movie = listbox.get(ANCHOR)

        # Delete from list that provided it
        selected_movie = selected_movie.split(":")
        key = selected_movie[0].strip()
        self.movies_dict.pop(key)

        # [TODO]: This is just for test, needs to go when app is finished!
        print(self.movies_dict)

def main():
    root = Tk()
    ex = MovieRatings(root)
    root.geometry("840x468+840+468")
    root.mainloop()


if __name__ == '__main__':
    main()
