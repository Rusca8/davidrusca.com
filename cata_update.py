import catagrames as cg

print("Actualitzant la frase del catagrama...")

try:
    cg.add_new_quote_to_archive()
except:
    print("No ha funcionat la cosa")
