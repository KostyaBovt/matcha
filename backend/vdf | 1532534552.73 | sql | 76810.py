
        select users.*, users_info.*, user_match.matched_interests, distances.distance, date_part('year', AGE(users_info.birth)) as "age", avatars_table.avatar_name
        from users
        inner join users_info on users.id = users_info.user_id
        inner join
            (select user_id, name as "avatar_name" 
            from photos
            where photos.avatar = 1) as avatars_table
        on users.id=avatars_table.user_id
        left join
            (select user_id, count(interests.interest) as matched_interests 
            from users_interests
            inner join interests on users_interests.interest_id=interests.id
            where interests.interest in ('some_blank_interest_to_avoid_error', 'football', 'dogs', 'science', 'food', 'FIFA', 'flowers')
            and not user_id=48
            group by user_id) as user_match
        on users.id=user_match.user_id
        inner join
            (select users_info.user_id, 2 * 3961 * asin(sqrt((sin(radians((users_info.geo_lat - 50.468431599999995) / 2))) ^ 2 + cos(radians(50.468431599999995)) * cos(radians(users_info.geo_lat)) * (sin(radians((users_info.geo_lng - 30.451862599999998) / 2))) ^ 2)) as distance
            from users_info
            where not user_id=48
            and users_info.geo_lat is not null
            and users_info.geo_lng is not null
            ) as distances
        on users.id=distances.user_id
        where not users.id=48
        and users_info.geo_lat is not null
        and users_info.geo_lng is not null
        and distance < 50.000000
		and users_info.gender=2
		and users_info.rating * 100 >= 0.000000
		and users_info.rating * 100 <= 100.000000
		and EXTRACT(year from AGE(users_info.birth)) >= 24
		and EXTRACT(year from AGE(users_info.birth)) <= 30
		order by user_match.matched_interests desc