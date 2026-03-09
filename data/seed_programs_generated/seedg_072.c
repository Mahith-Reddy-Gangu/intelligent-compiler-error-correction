int sub(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  x++;
  y--;
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
  int n = 5;
  int a[10];
  int b[n];
  a[0] = 1;
  b[1] = a[0] + 2;
  int t = a[0] + b[1];
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

int min2(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
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
  return 0;
}

int update(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  float fx = 1.25;
  float fy = 2.50;
  float fz = fx + fy;
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
  x++;
  y--;
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
  int n = 5;
  int a[10];
  int b[n];
  a[0] = 1;
  b[1] = a[0] + 2;
  int t = a[0] + b[1];
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

int blend(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
  x = !x;
  x = +x;
  x = -x;
  ++x;
  --y;
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
  sub(x);
  min2(x);
  update(x);
  blend(x);
  return 0;
}
