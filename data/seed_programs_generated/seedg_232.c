int mix()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3, p3;
  x++;
  y--;
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
  int n = 5;
  int a[10];
  int b[n];
  a[0] = 1;
  b[1] = a[0] + 2;
  int t = a[0] + b[1];
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
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

int divi()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3, p3;
  x++;
  y--;
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
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
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

int mul()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3, p3;
  x++;
  y--;
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
  int n = 5;
  int a[10];
  int b[n];
  a[0] = 1;
  b[1] = a[0] + 2;
  int t = a[0] + b[1];
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
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

int pick()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3, p3;
  x++;
  y--;
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
  int n = 5;
  int a[10];
  int b[n];
  a[0] = 1;
  b[1] = a[0] + 2;
  int t = a[0] + b[1];
  int m2[3][4];
  m2[1][2] = 7;
  int u = m2[1][2];
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
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
  mix(x, y, z);
  divi(x, y, z);
  mul(x, y, z);
  return 0;
}
