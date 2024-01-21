#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct User {
    char *username;
    char *password;
    int balance;
} User;

void registerUser(FILE *file) {
    User newUser;
    newUser.username = (char *)malloc(50 * sizeof(char));
    newUser.password = (char *)malloc(50 * sizeof(char));

    printf("Enter username: ");
    scanf("%s", newUser.username);

    printf("Enter password: ");
    scanf("%s", newUser.password);

    printf("Enter balance: ");
    scanf("%d", &newUser.balance);

    fprintf(file, "%s %s %d\n", newUser.username, newUser.password, newUser.balance);
    printf("Registration successful!\n");

    // Free allocated memory
    free(newUser.username);
    free(newUser.password);
}

int loginUser(FILE *file, User *loggedInUser) {
    char enteredUsername[50], enteredPassword[50];
    loggedInUser->username = (char *)malloc(50 * sizeof(char));
    loggedInUser->password = (char *)malloc(50 * sizeof(char));

    printf("Enter username: ");
    scanf("%s", loggedInUser->username);

    printf("Enter password: ");
    scanf("%s", loggedInUser->password);

    rewind(file);

    while (fscanf(file, "%s %s %d", enteredUsername, enteredPassword, &(loggedInUser->balance)) == 3) {
        if (strcmp(loggedInUser->username, enteredUsername) == 0 &&
            strcmp(loggedInUser->password, enteredPassword) == 0) {
            return 1; // Login successful
        }
    }

    // Free allocated memory
    free(loggedInUser->username);
    free(loggedInUser->password);

    return 0; // Login failed
}

int otpgen() {
    int randomNumber, userotp;
    srand(time(NULL));
    randomNumber = rand() % 9000 + 1000;
    printf("The 4-digit OTP number is: %d\n", randomNumber);
    printf("Enter the 4-digit OTP number: ");
    scanf("%d", &userotp);

    if (randomNumber == userotp) {
        printf("Congratulations! The OTP number is verified\n");
        return 1; // OTP verification successful
    } else {
        printf("Sorry, Enter the valid OTP number\n");
        return 0; // OTP verification failed
    }
}

void transferMoney(User *loggedInUser) {
    char get[50];
    int getmoney;
    printf("Enter Name to Transfer the Money: ");
    scanf(" %[^\n]", get);

    printf("Enter the Amount to be transferred: ");
    scanf("%d", &getmoney);

    if (getmoney <= loggedInUser->balance) {
        printf("Transfer successful! %d amount transferred to %s\n", getmoney, get);
        loggedInUser->balance -= getmoney;
    } else {
        printf("Insufficient balance for the transfer.\n");
    }
}

void logout(User *loggedInUser) {
    printf("Successfully Logged Out\n");

    // Free allocated memory for the logged-in user
    free(loggedInUser->username);
    free(loggedInUser->password);
}

int login() {
    int choice, flag = 0;
    User loggedInUser;
    FILE *file = fopen("D:\\users.txt", "a+");

    if (file == NULL) {
        printf("Error opening file\n");
        return 0;
    }

    do {
        printf("1. Register\n2. Login\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                registerUser(file);
                break;
            case 2:
                if (loginUser(file, &loggedInUser)) {
                    printf("Login successful!\n");
                    printf("Account Balance for %s: %d\n", loggedInUser.username, loggedInUser.balance);

                    if (otpgen()) {
                        transferMoney(&loggedInUser);
                        logout(&loggedInUser);
                        flag = 1;
                    }
                } else {
                    printf("Invalid username or password. Please try again.\n");
                }
                break;
            default:
                printf("Invalid choice. Please enter a valid option.\n");
        }
    } while (flag == 0);

    fclose(file);
    return 1;
}

int main() {
    int isLoggedIn = 0;

    isLoggedIn = login();

    if (isLoggedIn) {
        // Additional modules after successful login
    } else {
        printf("Login failed. Invalid credentials.\n");
    }

    return 0;
}
