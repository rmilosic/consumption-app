if [[ $# -eq 0 ]] 
then
	echo "no tag provided, exiting"
	exit 1
fi

tag=$1
echo "deployment tag $tag"


# fetch

git fetch --all


# checkout

git checkout --force $tag

# compose

docker compose -f compose.int.yaml up -d --no-deps --build django_app