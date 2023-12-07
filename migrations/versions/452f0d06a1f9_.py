"""empty message

Revision ID: 452f0d06a1f9
Revises: 
Create Date: 2023-12-07 01:23:33.095612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '452f0d06a1f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('ArtistID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Name', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('ArtistID')
    )
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_artist_Name'), ['Name'], unique=False)

    op.create_table('song',
    sa.Column('SongID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Title', sa.String(length=250), nullable=True),
    sa.Column('Genre', sa.String(length=250), nullable=True),
    sa.Column('Year', sa.Integer(), nullable=True),
    sa.Column('Upvotes', sa.Integer(), nullable=True),
    sa.Column('Downvotes', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('SongID')
    )
    with op.batch_alter_table('song', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_song_Genre'), ['Genre'], unique=False)
        batch_op.create_index(batch_op.f('ix_song_Title'), ['Title'], unique=False)
        batch_op.create_index(batch_op.f('ix_song_Year'), ['Year'], unique=False)

    op.create_table('user',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('userid')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('linking',
    sa.Column('SongID', sa.Integer(), nullable=False),
    sa.Column('ArtistID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ArtistID'], ['artist.ArtistID'], ),
    sa.ForeignKeyConstraint(['SongID'], ['song.SongID'], ),
    sa.PrimaryKeyConstraint('SongID', 'ArtistID')
    )
    op.create_table('userdissongs',
    sa.Column('SongID', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['SongID'], ['song.SongID'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('SongID', 'userid')
    )
    op.create_table('usersongs',
    sa.Column('SongID', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['SongID'], ['song.SongID'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('SongID', 'userid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usersongs')
    op.drop_table('userdissongs')
    op.drop_table('linking')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    with op.batch_alter_table('song', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_song_Year'))
        batch_op.drop_index(batch_op.f('ix_song_Title'))
        batch_op.drop_index(batch_op.f('ix_song_Genre'))

    op.drop_table('song')
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_artist_Name'))

    op.drop_table('artist')
    # ### end Alembic commands ###
