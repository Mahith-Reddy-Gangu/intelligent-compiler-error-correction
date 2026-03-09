int rangeSum()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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

int add()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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

int accum()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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

int qux()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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

int clamp()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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

int main()
{
  int x = 1;
  int y = 2;
  int z = 3;
  ;
  rangeSum(x, y);
  add(x, y);
  accum(x, y);
  return 0;
}
