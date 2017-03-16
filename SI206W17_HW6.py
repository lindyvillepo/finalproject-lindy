###################
import json
import unittest
import random

## As usual, this HW is worth 500 points in total.
## There are 10 problems. Each one is worth 50 points.

## There are tests for each problem; you should also follow the instructions for things to do in the code that cannot be tested with unit tests, e.g. using certain structures.
## Name: Lindy Villeponteau

## [PROBLEM 1]
print("\n\n***** Problem 1 *****")
## We've provided a definition of a class Student, similar to the one you may have seen in lecture. 
## Add a method to class Student called write_programs which accepts one optional parameter with a default value of 1, and adds the input integer to the self.num_programs instance variable.

class Student():
    def __init__(self, name, years_at_umich=1, programs_written=0):
        self.name = name
        self.years_UM = years_at_umich
        self.bonus_points = random.randrange(1000)
        self.num_programs = programs_written

    def shout(self, phrase_to_shout):
        print(phrase_to_shout)  # print is for ppl!

    def __str__(self):
        return "My name is {}, and I've been at UMich for about {} years. I got {} bonus_points and I have written {} programs while here.".format(self.name, self.years_UM, self.bonus_points, self.num_programs)

    def year_at_umich(self):
        return this_Student.years_UM

    # Define the additional method here
    def write_programs(self, value=1):
        self.num_programs += value

#### DONE WITH STUDENT CLASS DEFINITION

    
print("===========")
## Code to show how this works...s
pst = Student("Jay", 3, 2)
print(pst)  # This should print: My name is Jay, and I've been at UMich for about 3 years. I got <some number 0-1000> of bonus points and I have written 2 programs while here.
pst.shout("I'm doing awesome on this problem set.")  # This should print: I'm doing awesome on this problem set.

## Feel free to add more testing code here to help you understand the class definition, especially to try out your write_programs method...


print("===========")

## [PROBLEM 2]
print("\n\n***** Problem 2 *****")

## Define a function called personal_map. This function should do a very similar thing to the Python built-in map function.
## It should take as input one function object (required), and one list (required), in that order.
## The function should invoke the input function upon each element of the input list, and accumulate the return values to a new list.
## The function should return the new list of accumulated -- mapped! -- values.
## HINT: you should be able to write this in 5 lines of code or fewer! 
def personal_map(a_function, a_list):
    new_list = list(map(a_function, a_list))
    return new_list

## [PROBLEM 3]
print("\n\n***** Problem 3 *****")

## We've provided the function access_third_elem. Write a lambda function that does exactly the same thing as access_third_elem (you can assume any input it would receive has at least 3 elements in it). Assign that lambda function to the variable sample_func.

## Note that we cannot specifically test in the unit tests whether it is a lambda function, but you will not get points for this question unless it is.

## Provided, do not change:
def access_third_elem(seq):
    return seq[2]
## End

# Write your equivalent function and assignment statement here
def sample_func(seq):
    return ((lambda x: x[2])(seq))

## [PROBLEM 4]
print("\n\n***** Problem 4 *****")

## Provided code
names = ["Albert", "Bisi", "Mai", "Dinesh", "Euijin"]
seniority = [1, 5, 2, 4, 3]
programs_written = [10, 500, 20, 131, 46]
## End provided code

# Given that provided code, write one line of code to create a zip iterator instance saved in a variable called student_tups, here:
student_tups = zip(names, seniority, programs_written)

# Then write a line of code to cast the iterator to a list (it should end up as a list of tuples). Save that list in a variable called student_tups_list.
student_tups_list = list(student_tups)

## You can test this out with any code you like here, and similar below other problems, but make sure to comment out any code that uses up the iterator in order to pass the tests!




##### TESTS BELOW THIS LINE. DO NOT CHANGE ANY CODE BELOW THIS LINE. #####
print("\n\nOUTPUT FROM TESTS SHOWN BELOW THIS LINE.\n\n")

class Problem1(unittest.TestCase):
    def test_write_progs1(self):
        s = Student("Name",1,1)
        s.write_programs()
        self.assertEqual(s.num_programs,2)
    def test_write_progs2(self):
        s = Student("Name2",2,2)
        s.write_programs(8)
        self.assertEqual(s.num_programs, 10)
    def test_write_progs3(self):
        s = Student("Name3",3,3)
        s.write_programs(0)
        self.assertEqual(s.num_programs, 3)

class Problem2(unittest.TestCase):
    def test_personal_map(self):
        self.assertEqual(personal_map(lambda x:len(x),["hi","hello"]),[2,5])
    def test_personal_map2(self):
        def complex(inp):
            if inp > 7:
                return 14
            elif inp < 3:
                return "small"
            else:
                return 0.2
        self.assertEqual(personal_map(complex,[9,3,1,0]),[14,0.2,"small","small"])

class Problem3(unittest.TestCase):
    def test_sample_func(self):
        self.assertEqual(sample_func([1,2,3]),3)
    def test_sample_func2(self):
        self.assertEqual(sample_func([0,3243,2343,23,342,23432,23423,43235,2343]),2343)

class Problem4(unittest.TestCase):
    def test_student_tups_iterator(self):
        self.assertEqual(type(student_tups),type(zip([1,2],[3,4])))
    def test_student_tups_list(self):
        self.assertEqual(student_tups_list,[('Albert', 1, 10), ('Bisi', 5, 500), ('Mai', 2, 20), ('Dinesh', 4, 131), ('Euijin', 3, 46)])

class Problem5(unittest.TestCase):
    def test_programmers_list(self):
        self.assertEqual(type(programmers),type([]))
    def test_programmers_list2(self):
        self.assertEqual(type(programmers[2]),type(Student("Jess")))
    def test_programmers_list3(self):
        self.assertEqual([x.name for x in programmers],["Albert","Bisi","Mai","Dinesh","Euijin"])

class Problem6(unittest.TestCase):
    def test_prod_iter(self):
        self.assertEqual(type(prod_iter),type(map(lambda x:-x,[2,3])))
    def test_prod_list(self):
        self.assertEqual(prod_list,[10.0,100.0,10.0,32.75,15.333333333333334])

# class Problem7(unittest.TestCase):
    def test_names_and_productivities(self):
        self.assertEqual(names_and_productivities,[('Albert', 10.0), ('Bisi', 100.0), ('Mai', 10.0), ('Dinesh', 32.75), ('Euijin', 15.333333333333334)])

class Problem8(unittest.TestCase):
    def test_long_names(self):
        self.assertEqual(type(filter(lambda x: x>2,[2,5])),type(long_names))
    def test_long_names_list(self):
        self.assertEqual(type(long_names_list),type([]))
    def test_long_names_list_instances(self):
        self.assertEqual(type(long_names_list[1]),type(Student("Dinah")))
    def test_long_names_list2(self):
        self.assertEqual([x.name for x in long_names_list],["Albert","Dinesh","Euijin"])

class Problem9(unittest.TestCase):
    def test_names_without_much_seniority(self):
        self.assertEqual(names_with_not_too_much_seniority,['Albert', 'Mai', 'Dinesh', 'Euijin'])

class Problem10(unittest.TestCase):
    def test_generator1(self):
        self.assertEqual(list(readfiles(["samplehw6_1.txt","samplehw6_2.txt"])),['hihihi\n', 'this is a very long line that is more than thirty or forty characters long\n', 'supercalifragilistic\n', 'supercalifragilisticexpialidocioussupercalifragilisticexpialidocious', '\n', 'Where Does the Dance Begin, Where Does It End?\n', '\n', "Don't call this world adorable, or useful, that's not it.\n", "It's frisky, and a theater for more than fair winds.\n", 'The eyelash of lightning is neither good nor evil.\n', 'The struck tree burns like a pillar of gold.\n', '\n', 'But the blue rain sinks, straight to the white\n', 'feet of the trees\n', 'whose mouths open.\n', "Doesn't the wind, turning in circles, invent the dance?\n", "Haven't the flowers moved, slowly, across Asia, then Europe,\n", 'until at last, now, they shine\n', 'in your own yard?\n', '\n', "Don't call this world an explanation, or even an education.\n", '\n', 'When the Sufi poet whirled, was he looking\n', 'outward, to the mountains so solidly there\n', 'in a white-capped ring, or was he looking\n', '\n', 'to the center of everything: the seed, the egg, the idea\n', 'that was also there,\n', 'beautiful as a thumb\n', 'curved and touching the finger, tenderly,\n', 'little love-ring,\n', '\n', 'as he whirled,\n', 'oh jug of breath,\n', 'in the garden of dust?\n', '\n', '-Mary Oliver'], "Testing that readfiles works correctly")
    def test_generator2(self):
        self.assertEqual(list(len_check(readfiles(["samplehw6_1.txt","samplehw6_2.txt"]))),['this is a very long line that is more than thirty or forty characters long\n', 'supercalifragilisticexpialidocioussupercalifragilisticexpialidocious', 'Where Does the Dance Begin, Where Does It End?\n', "Don't call this world adorable, or useful, that's not it.\n", "It's frisky, and a theater for more than fair winds.\n", 'The eyelash of lightning is neither good nor evil.\n', 'The struck tree burns like a pillar of gold.\n', 'But the blue rain sinks, straight to the white\n', "Doesn't the wind, turning in circles, invent the dance?\n", "Haven't the flowers moved, slowly, across Asia, then Europe,\n", "Don't call this world an explanation, or even an education.\n", 'When the Sufi poet whirled, was he looking\n', 'outward, to the mountains so solidly there\n', 'in a white-capped ring, or was he looking\n', 'to the center of everything: the seed, the egg, the idea\n', 'curved and touching the finger, tenderly,\n'])


if __name__ == "__main__":
    unittest.main(verbosity=2)