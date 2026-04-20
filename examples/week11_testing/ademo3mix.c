int add(int a, int b) {
    return a + b;
}

int sub(int a, int b) {
    return a - b;
}

int mul(int a, int b) {
    return a * b;
}

int syntax1() {
    int a = 5
    return a;
}

int syntax2() {
    int arr[5;
    return 0;
}

int syntax3() {
    int x = add(10 20);
    return x;
}

int syntax4(int a int b) {
    return a + b;
}

int syntax5() {
    int a = 0;
    whlie (a < 5) {
        a = a + 1;
    }
    return a;
}

int syntax6() {
    int i = 0;
    int s = 0;
    fro (i = 0; i < 5; i = i + 1) {
        s = s + i;
    }
    return s;
}

int syntax7() {
    int i = 0;
    int s = 0;
    for (i = 0; i < 5 i = i + 1) {
        s = s + i;
    }
    return s;
}

int syntax8() {
    int a = 5;
    if (a > 3) {
        a = a + 1;
    }
    esle {
        a = a - 1;
    }
    return a;
}

int syntax9() {
    int a = 5;
    if a > 3) {
        return a;
    }
    return 0;
}

int syntax10() {
    int a = 5;
    if (a > 3 {
        return a;
    }
    return 0;
}

int syntax11() {
    int a = 0;
    while (a < 5) {
        if (a == 2) {
            break
        }
        a = a + 1;
    }
    return a;
}

int syntax12() {
    int a = 0;
    while (a < 5) {
        a = a + 1;
        if (a == 2) {
            continue
        }
    }
    return a;
}

int syntax13() {
    cahr x = 'a';
    return 0;
}

viod helper14() {
    return;
}

int syntax15() {
    int z = add(3, 4;
    return z;
}

int syntax16() {
    int z = add(add(1 2), 3);
    return z;
}

int syntax17() {
    int z = add(add(1, 2), 3;
    return z;
}

int syntax18() {
    int a[5];
    int b = a[0;
    return b;
}

int syntax19() {
    int x = 1
    int y = 2;
    return x + y;
}

int syntax20() {
    int a = 0;
    while a < 5) {
        a = a + 1;
    }
    return a;
}

/* isolated security cases */

int sec1() {
    char buf[32];
    gets(buf);
    return 0;
}

int sec2() {
    char s[20];
    scanf("%s", s);
    return 0;
}

int sec3() {
    char cmd[40];
    scanf("%s", cmd);
    system(cmd);
    return 0;
}

/* only one mild mixed case */

int mix1() {
    int a = 5
    char buf[20];
    gets(buf);
    return a;
}

int block1() {
    int total = 0;
    total = total + syntax1();
    total = total + syntax2();
    total = total + syntax3();
    total = total + syntax4(1, 2);
    total = total + syntax5();
    return total;
}

int block2() {
    int total = 0;
    total = total + syntax6();
    total = total + syntax7();
    total = total + syntax8();
    total = total + syntax9();
    total = total + syntax10();
    return total;
}

int block3() {
    int total = 0;
    total = total + syntax11();
    total = total + syntax12();
    total = total + syntax13();
    helper14();
    total = total + syntax15();
    return total;
}

int block4() {
    int total = 0;
    total = total + syntax16();
    total = total + syntax17();
    total = total + syntax18();
    total = total + syntax19();
    total = total + syntax20();
    return total;
}

int block5() {
    int total = 0;
    total = total + sec1();
    total = total + sec2();
    total = total + sec3();
    total = total + mix1();
    return total;
}

int main() {
    int total = 0;
    int arr[5];
    int i = 0;

    arr[0] = block1();
    arr[1] = block2();
    arr[2] = block3();
    arr[3] = block4();
    arr[4] = block5();

    while (i < 5) {
        total = total + arr[i];
        i = i + 1;
    }

    total = total + mul(2, 3);

    return total;
}