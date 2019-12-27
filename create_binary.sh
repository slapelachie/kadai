cd ./src/
zip -r ../kadai.zip *
cd ..
echo '#!/usr/bin/env python' | cat - kadai.zip > kadai
chmod +x kadai
rm kadai.zip