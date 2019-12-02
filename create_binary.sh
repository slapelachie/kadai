cd ./src/
zip -r ../kadai.zip *
cd ..
echo '#!/usr/bin/env python' | cat - kadai.zip > kadai
rm kadai.zip