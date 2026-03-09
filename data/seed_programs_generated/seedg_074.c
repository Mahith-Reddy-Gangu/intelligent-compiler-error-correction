int emit(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1;
  char ch = 'a';
  char nl = '\n';
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
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

int update(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1;
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
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

int add(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1;
  char ch = 'a';
  char nl = '\n';
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
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

int divi(int a0, int b1, float f2)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1;
  char ch = 'a';
  char nl = '\n';
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  if (x <= y) { z = z + 1; }
  if (z != 0) { z = z - 1; }
  if (x == 1) { z = z * 2; }
  if (y >= 2) { z = z / 2; }
  if ((x < y) && (z > 0)) { z += 1; }
  if ((x == 0) || (y == 2)) { z -= 1; }
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
  x = (x = x + 1, y = y + 2, z);
  if (x < y) {
    z = z + 1;
  } else {
    z = z + 2;
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
  emit(x, y, z);
  update(x, y, z);
  add(x, y, z);
  divi(x, y, z);
  return 0;
}
