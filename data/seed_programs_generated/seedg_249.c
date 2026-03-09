int clamp()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
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

int mix()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
  }
  for (int i = 0; i < 3; ) {
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

int mul()
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1, p1, p2 = 3;
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
  while (x < 3) {
    x++;
    if (x == 2) {
      continue;
    }
    if (x == 3) {
      break;
    }
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

int main()
{
  int x = 1;
  int y = 2;
  int z = 3;
  ;
  clamp(x, y);
  mix(x, y);
  mul(x, y);
  return 0;
}
