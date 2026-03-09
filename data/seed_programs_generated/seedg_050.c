int bar(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
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

int divi(int a0, int b1)
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
  return 0;
}

int clamp(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
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

int score(int a0, int b1)
{
  int x = 1;
  int y = 2;
  int z = 3;
  int p0 = 1;
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
  int m = (x < y) ? x : y;
  z = (m == 1) ? (z + 1) : (z + 2);
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
  bar(x, y, z);
  divi(x, y, z);
  clamp(x, y, z);
  score(x, y, z);
  return 0;
}
