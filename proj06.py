""" Source header """

import sys
import csv

def input( prompt=None ):
    if prompt:
        print( prompt, end="" )
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip( "\n" )
    print( aaa_str )
    return aaa_str

choices = '''
  Menu : 
     1: Max number of friends intersection between X and Facebook among all
     2: Percentage of people with no shared friends between X and Facebook
     3: Individual information
     4: Percentage of people with  more friends in X compared to Facebook
     5: The number of  triangle friendships in X
     6: The number of  triangle friendships on Facebook
     7: The number of  triangle friendships in X and Facebook together 
       Enter any other key(s) to exit

  '''



def open_file(prompt):
    while True:
        try:
            filename = input(prompt)
            return open(filename, "r")
        except:
            print("Error. File does not exist")

def read_names_file():
    names = []
    name_file_fp = csv.reader(open_file("\nEnter a names file ~:"))
    for line in name_file_fp:
        names.append(line[0])
    return names

def read_x_names_file(prompt, names):
    file = open_file(prompt)
    list_of_list = []
    list = []
    real_names = []

    for line in file:
        list = line.strip().split(",")
        list = list[:-1]
        list_of_list.append(list)

    for i in range(len(list_of_list)):
        real_friends = []
        for x in range(len(list_of_list[i])):
            username = names[int(list_of_list[i][x])]
            real_friends.append(username)
        real_names.append(real_friends)
    return real_names

def read_fb_names_file(prompt):
    fb_friends = []
    fb_fp = open_file(prompt)
    for line in fb_fp:
        fb_friends.append(line.split(","))
    for list in fb_friends:
        list.pop()
    return fb_friends

def create_nest_dict(names, x_friends, fb_friends):
    nest_dict = {}
    for i in range(len(names)):
        nest_dict[names[i]] = {'Twitter': x_friends[i], 'Facebook': fb_friends[i]}
    return nest_dict

def max_ints(nest_dict):
    max_ints = 0
    for name, friends in nest_dict.items():
        ints_count = len(set(friends['Twitter']).intersection(friends['Facebook']))
        if ints_count > max_ints:
            max_ints = ints_count
    return max_ints

def no_friends(nest_dict):
    no_friends = 0
    total = len(nest_dict)
    for name, friends in nest_dict.items():
        if len(set(friends['Twitter']).intersection(friends['Facebook'])) == 0:
            no_friends += 1
    return (no_friends / total) * 100

def individual(nest_dict):
    rand_bool = True
    while rand_bool == True:
        ind_name = input("Enter a person's name ~:")
        if ind_name in nest_dict:
            print("--------------")
            print("Friends in X")
            print("**************")
            nest_dict[ind_name]['Twitter'].sort()
            nest_dict[ind_name]['Facebook'].sort()
            for friend in nest_dict[ind_name]['Twitter']:
                print(friend)
            print("--------------------")
            print("Friends in Facebook")
            print("********************")
            for friend in nest_dict[ind_name]['Facebook']:
                print(friend)
            rand_bool = False
        else:
            print("Invalid name or does not exist")

def friends_percentage(nest_dict):
    more_x_friends = 0
    total = len(nest_dict)
    for name, friends in nest_dict.items():
        if len(friends['Twitter']) > len(friends['Facebook']):
            more_x_friends += 1
    return ((more_x_friends / total) * 100)

def x_triangle(nest_dict):
    triangles = []
    triangle_count = 0
    for name, friends in nest_dict.items():
        for x_friend in friends['Twitter']:
            for x_friend2 in nest_dict[x_friend]['Twitter']:
                if x_friend2 in nest_dict and name in nest_dict[x_friend2]['Twitter']:
                    triangle = [name, x_friend, x_friend2]
                    triangle.sort()
                    if triangle not in triangles:
                        triangles.append(triangle)
                        triangle_count += 1
    return triangle_count

def fb_triangle(nest_dict):
    triangles = []
    triangle_count = 0
    for name, friends in nest_dict.items():
        for fb_friend in friends['Facebook']:
            for fb_friend2 in nest_dict[fb_friend]['Facebook']:
                if fb_friend2 in nest_dict and name in nest_dict[fb_friend2]['Facebook']:
                    triangle = [name, fb_friend, fb_friend2]
                    triangle.sort()
                    if triangle not in triangles:
                        triangles.append(triangle)
                        triangle_count += 1
    return triangle_count

def merged_triangle(nest_dict):
    triangles = []
    triangle_count = 0
    for name, friends in nest_dict.items():
        total_friends = set(friends['Twitter']).union(friends['Facebook'])
        for f1 in total_friends:
            for second_friend in total_friends:
                if second_friend != f1:
                    if second_friend in nest_dict:
                        if f1 in nest_dict[second_friend].get('Twitter', []) + nest_dict[second_friend].get('Facebook', []):
                            triangle = [name, f1, second_friend]
                            triangle.sort()
                            if triangle not in triangles:
                                triangles.append(triangle)
                                triangle_count += 1
    return triangle_count

def main():
    names = read_names_file()
    x_friends = read_x_names_file("\nEnter the twitter id file ~:",names)
    fb_friends = read_fb_names_file("\nEnter the facebook id file ~:")
    nest_dict = create_nest_dict(names, x_friends, fb_friends)
    loop_bool = True
    while loop_bool == True:
        print(choices)
        choice = input("Input a choice ~:")
        if choice == '1':
            print(f"The Max number intersection of friends between X and Facebook is: {max_ints(nest_dict)}")
        elif choice == '2':
            print("{:.0f}% of people have no friends in common on X and Facebook".format(no_friends(nest_dict)))
        elif choice == '3':
            individual(nest_dict)
        elif choice == '4':
            print("{:.0f}% of people have more friends in X compared to Facebook".format(friends_percentage(nest_dict)))
        elif choice == '5':
            print(f"The number of triangle friendships in X is: {x_triangle(nest_dict)}")
        elif choice == '6':
            print(f"The number of triangle friendships in Facebook is: {fb_triangle(nest_dict)}")
        elif choice == '7':
            print(f"The number of triangle friendships in X merged with Facebook is:  {merged_triangle(nest_dict)}")
        else:
            print("Thank you")
            sys.exit()



if __name__ == '__main__':
    main()

