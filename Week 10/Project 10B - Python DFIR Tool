import os
import hashlib
import csv
import psutil

# Set the location of output file to the current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))



class Dfir:
    def generate_fingerprints(self) -> None:
        """Generate fingerprints (checksums) of all the python files in the current directory
        """
        file_list = os.listdir()
        checksums = open('checksums.csv', 'w')
        checksums_writer = csv.writer(checksums, delimiter=',')
        for file_name in file_list:
            # We will generate the fingertips of only Python files for now
            if file_name.endswith('.py'):
                with open(file_name, 'r') as file:
                    plain_text = file.read()
                    hashed_text = hashlib.sha256(plain_text.encode()).hexdigest()
                    print(file_name, ', ', hashed_text)
                    checksums_writer.writerow([file_name, hashed_text])
        checksums.close()

    def compare_fingerprints(self) -> bool:
        """Compares the fingertips (checksum) of all the python files in the current directory with what was generated before
        and shows if the results are ok or they don't match"""
        mismatch_found = False
        file_list = os.listdir()
        checksums = open('checksums.csv', 'r')
        checksums_reader = csv.reader(checksums, delimiter=',')
        # Create a dictionary out of the csv file for all the checksums
        mydict = {}
        for rows in checksums_reader:
            if len(rows) >= 2:  # Ensure the row has at least two elements
                mydict[rows[0]] = rows[1]
        checksums.close()  # Close the file after reading
        for file_name in file_list:
            if file_name.endswith('.py'):
                with open(file_name, 'r') as file:
                    plain_text = file.read()
                    hashed_text = hashlib.sha256(plain_text.encode()).hexdigest()
                    if mydict.get(file_name) == hashed_text:
                        print(file_name, ': OK')
                    else:
                        print(file_name, ': Mismatch')
                        mismatch_found = True
        return mismatch_found

    def get_last_logins_not_current_user(self, authorized_user) -> bool:
        """Find out if any of the logged in users are not the same as the specified user
        Returns:
            _type_: _description_
        """
        unauthorized_user_found = False
        # Get a list of tuples containing all the current (logged in) users
        current_users = psutil.users()
        for user in current_users:
            if user[0] != authorized_user:
                print('Unauthorized user found: ', user[0])
                unauthorized_user_found = True
            else:
                print(user[0], 'is an authorized user')
        return unauthorized_user_found

if __name__ == '__main__':
    response = Dfir()
    response.generate_fingerprints()  
    if response.compare_fingerprints():
        print('----Fingerprint mismatch found\n')
    else:
        print('----No fingerprint mismatch found\n')
    if response.get_last_logins_not_current_user(os.getlogin()): # <--- This gets your Microsoft login username.
        print('Unauthorized user found\n')
    else:
        print('----No unauthorized user found\n')
