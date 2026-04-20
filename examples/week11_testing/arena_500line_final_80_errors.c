int arena_max2(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}
int arena_min2(int a, int b) {
    if (a < b) {
        return a;
    }
    return b;
}
int arena_sum3(int a, int b, int c) {
    return a + b + c;
}
int arena_solve_0(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_1(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_2(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_3(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_4(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_5(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_6(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_7(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_8(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_9(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_10(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_11(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_12(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_13(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_14(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_15(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_16(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    whlie (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best) {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int arena_solve_17(int n, int q, int bias) {
    int arr[8];
    int i = 0;
    int ans = 0
    int best = 0;
    int low = 0
    for (i = 0; i < 8; i = i + 1) {
        arr[i] = i + bias + q;
    }
    best = arr[0];
    low = arr[0];
    i = 0;
    while (i < n) {
        if (i < q) {
            ans = ans + arena_sum3(arr[i % 8], bias, q);
        }
        else {
            ans = ans + arena_max2(arr[i % 8], bias);
        }
        if (ans > best {
            best = ans;
        }
        if (ans < low) {
            low = ans;
        }
        i = i + 1;
    }
    ans = ans + arena_min2(best, low);
    return ans;
}
int main() {
    int n = 6;
    int q = 3;
    int bias = 2;
    int answer = 0;
    int i = 0
    prinft("start");
    while (i < 18 {
        answer = answer + arena_solve_0(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_1(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_2(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_3(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_4(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_5(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_6(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_7(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_8(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_9(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_10(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_11(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_12(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_13(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_14(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_15(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_16(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        answer = answer + arena_solve_17(n, q, bias);
        n = n + 1;
        q = q + 1;
        bias = bias + 1;
        if (bias > 7) {
            bias = 2;
        }
        i = i + 1;
    }
    prinft("done");
    return answer;
}
