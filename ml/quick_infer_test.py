from compiler.ai_error_corrector import ai_correct_source_patch_mode

bad = """int main(){
int x
return 0;
}
"""

# simulate parser error location (you can change line/col to test)
# line numbers are 1-based, col is 0-based
fixed, cmd = ai_correct_source_patch_mode(bad, error_line=2, error_column=5)

print("CMD:", cmd)
print("----- FIXED -----")
print(fixed)