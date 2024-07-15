from db.mysql_requests import get_clusters
from db.mysql_requests import get_platforms_from_cluster
from db.mysql_requests import insert_new_junctions
from typing import List, Tuple


clusters: List[int] = get_clusters()
routes_to_add: Tuple[Tuple] = []
for id_cluster in clusters:
    platforms: List[int] = get_platforms_from_cluster(id_cluster)
    for id_platform_from in platforms:
        for id_platform_to in platforms:
            if (id_platform_from != id_platform_to):
                routes_to_add.append((id_platform_from, id_platform_to, 0))
insert_new_junctions(routes_to_add)