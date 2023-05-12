echo can use this script to commit to git? or use gitpython? Need UIDs for remote artifacts somewhere!
export VERSION=$(awk -F "=" '/version/ {print $2}' tests/data/_verison.py | sed 's/ //g')
echo Building release: $VERSION
git checkout -b release-demo/${VERSION}
git add .
git commit -m "mlops automated release commit"
git push