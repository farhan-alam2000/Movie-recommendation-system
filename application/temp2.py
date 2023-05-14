def correct_movie_name(movie_name):
    movie_name = "Contractor Agent, A"
    movie_name_array = movie_name.split(',')
    print(movie_name_array)
    if(movie_name_array[1] == " The" or movie_name_array[1] == " A" or movie_name_array[1] == " An"):
        return (movie_name_array[1] + ' ' + movie_name_array[0])
    else: 
        return movie_name


# print(correct_movie_name("F/X 2"))

def read_most_popular(genre):
    