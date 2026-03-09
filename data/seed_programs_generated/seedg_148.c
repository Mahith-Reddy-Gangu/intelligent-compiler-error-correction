int test(int a0)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  int i = 0;
  for (i = 0; i < 3; i++) {
    if (i == 1) {
      ;
    }
    z += i;
    if (i == 2) {
      continue;
    }
    if (i == 3) {
      break;
    }
  }
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      z += (i + j);
      if ((i == 1) && (j == 2)) {
        break;
      }
    }
  }
  return 0;
}

int fold(int a0)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  int i = 0;
  for (i = 0; i < 3; i++) {
    if (i == 1) {
      ;
    }
    z += i;
    if (i == 2) {
      continue;
    }
    if (i == 3) {
      break;
    }
  }
  return 0;
}

int sum3(int a0)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  int i = 0;
  for (i = 0; i < 3; i++) {
    if (i == 1) {
      ;
    }
    z += i;
    if (i == 2) {
      continue;
    }
    if (i == 3) {
      break;
    }
  }
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      z += (i + j);
      if ((i == 1) && (j == 2)) {
        break;
      }
    }
  }
  return 0;
}

int accum(int a0)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  int i = 0;
  for (i = 0; ; i++) {
    if (i == 1) {
      ;
    }
    z += i;
    if (i == 2) {
      continue;
    }
    if (i == 3) {
      break;
    }
  }
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      z += (i + j);
      if ((i == 1) && (j == 2)) {
        break;
      }
    }
  }
  return 0;
}

int choose(int a0)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  int i = 0;
  for (i = 0; i < 3; i++) {
    if (i == 1) {
      ;
    }
    z += i;
    if (i == 2) {
      continue;
    }
    if (i == 3) {
      break;
    }
  }
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      z += (i + j);
      if ((i == 1) && (j == 2)) {
        break;
      }
    }
  }
  return 0;
}

int main()
{
  int x = 1;
  int y = 2;
  int z = 3;
  ;
  test(x, y, z);
  fold(x, y, z);
  sum3(x, y, z);
  return 0;
}
