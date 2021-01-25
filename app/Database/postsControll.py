from app import db, app
from app.models import Post, followers, User


def get_all_posts(filters=None, page=1, posts_per_page=app.config['POSTS_PER_PAGE']):
    if filters:
        filter_value = filters.get('sort_by', None)
        if not filter_value:
            q_r = Post.query.order_by(Post.timespan.desc()).paginate(
                page, posts_per_page, False)
        else:
            if filter_value == 'world':
                q_r = Post.query.order_by(Post.timespan.desc()).paginate(
                    page, posts_per_page, False)

            elif filter_value == 'country':
                q_r = Post.query.order_by(Post.timespan.desc()).paginate(
                    page, posts_per_page, False)

            elif filter_value == 'following':
                user_id = filters.get('user_id', None)
                if not user_id:
                    raise ValueError('Cant find following posts for user with id None')

                q_r = get_following_posts(user_id).paginate(
                    page, posts_per_page, False)
            else:
                q_r = Post.query.order_by(Post.timespan.desc()).paginate(
                    page, posts_per_page, False)
    else:
        q_r = Post.query.order_by(Post.timespan.desc()).paginate(
                page, posts_per_page, False)

    return q_r.items, q_r.has_prev, q_r.has_next, q_r.prev_num, q_r.next_num


def get_following_posts(follower_id):
    follower_posts = Post.query.filter_by(user_id=follower_id)
    following_posts = Post.query.join(
        followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == follower_id)

    return following_posts.union(follower_posts).order_by(Post.timespan.desc())





