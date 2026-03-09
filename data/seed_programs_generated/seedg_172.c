int clamp(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  char ch = 'a';
  char nl = '\n';
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  for (int i = 0; i < 3; i++) {
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

int dec(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  char ch = 'a';
  char nl = '\n';
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
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
  for (int i = 0; i < 3; i++) {
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

int sub(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  char ch = 'a';
  char nl = '\n';
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
  x += 1;
  y -= 1;
  z *= 2;
  z /= 2;
  z %= 3;
  x = (x = x + 1, y = y + 2, z);
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
  }
  for (int i = 0; i < 3; i++) {
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

int bar(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  char ch = 'a';
  char nl = '\n';
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
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
  for (int i = 0; i < 3; i++) {
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

int main()
{
  int x = 1;
  int y = 2;
  int z = 3;
  ;
  clamp(x, y);
  dec(x, y);
  sub(x, y);
  bar(x, y);
  return 0;
}
