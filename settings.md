# Config

These settings are mandatory

| Key                                               | Description                                                                                                                               | Examples                                                           | Default                                 |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------- |
| `config.site.display_name`                        | When displaying to the user, this is the name of the api                                                                                  | `Open Booru`, `Gelbooru`                                           | `Open Booru`                            |
| `config.site.hostname`                            | The hostname to use when providing links                                                                                                  | `localhost`, `api.openbooru.org`                                   | `localhost`                             |
| `config.site.post`                                | The port to host the api on                                                                                                               | `443`, `8080`                                                      | `8080`                                  |
| `config.ssl.enabled`                              | Make use of https?                                                                                                                        | `localhost`, `api.openbooru.org`                                   | `false`                                 |
| `config.ssl.key`                                  | The path to the ssl key file                                                                                                              | `~/server.key`, `./data/server.key`                                | `./data/server.key`                     |
| `config.ssl.cert`                                 | The path to the ssl cert file                                                                                                             | `~/server.crt`, `./data/server.crt`                                | `./data/server.crt`                     |
| `config.hcaptcha.enabled`                         | Should [hcaptcha](https://www.hcaptcha.com/) be required for verified endpoints                                                           | `false`, `true`                                                    | `false`                                 |
| `config.hcaptcha.sitekey`                         | The hcaptcha sitekey                                                                                                                      | `ffffffff-ffff-ffff-ffff-ffffffffffff`                             |                                         |
| `config.hcaptcha.secret`                          | The hcaptcha secret                                                                                                                       | `0xfffffffffffffffffffffffffffffffffffffffff`                      |                                         |
| `config.aws.id`                                   | Your AWS access key ID                                                                                                                    | `FFFFFFFFFFFFFFFFFFFF`                                             |                                         |
| `config.aws.secret`                               | Your AWS secret key                                                                                                                       | `ffffffffffffffff/ffffffffffffffffffffff`                          |                                         |
| `config.aws.region`                               | The AWS region to use                                                                                                                     | `eu-west-2`                                                        |                                         |
| `config.mongodb.hostname`                         | The hostname of the mongodb server                                                                                                        | `localhost`                                                        | `localhost`                             |
| `config.mongodb.port`                             | The port of the mongodb server                                                                                                            | `27017`                                                            | `27017`                                 |
| `config.mongodb.name`                             | What database name to use in mongodb                                                                                                      | `openbooru`                                                        | `openbooru`                             |
| `config.mongodb.username`                         | The username to login into the database with                                                                                              | `username`                                                         |                                         |
| `config.mongodb.password`                         | The password to login into the database with                                                                                              | `password`                                                         |                                         |
| `config.wipe_on_startup`                          | Wipe all the databases on startup, useful for testing                                                                                     | `false`, `true`                                                    | `false`                                 |
| `settings.database.choice`                        | Which database to use                                                                                                                     | `mongodb`                                                          | `mongodb`                               |
| `email.template_paths.email_verification`         | The email template used in account signup to verify a user owns an account                                                                | `./data/emails/email_verification.html`                            | `./data/emails/email_verification.html` |
| `email.template_paths.password_reset`             | The email template used to reset a user's password                                                                                        | `./data/emails/password_reset.html`                                | `./data/emails/password_reset.html`     |
| `posts.search.default_sort`                       | The default sort method if none is specified                                                                                              | `id`, `created_at`, `views`, `upvotes`, `downvotes`                | `created_at`                            |
| `posts.search.max_limit`                          | Max number of results users a user gets per search                                                                                        | `100`, `200`                                                       | `100`                                   |
| `tags.minimum_count`                              | Minumum count for the tag before it has an entry created                                                                                  | `0`, `20`                                                          | `5`                                     |
| `tags.tagging_service.enabled`                    | Should the server make use of an AI tagging service such as deep danbooru or hydrus-dd                                                    | `null`, `http://localhost:4443`                                    | `null`                                  |
| `tags.tagging_service.url`                        | The url for the tagging service to be used                                                                                                | `null`, `http://localhost:4443`                                    | `null`                                  |
| `import.local.enabled`                            | Import a set of local images. To import tags, have a file with the same name as image ending in `.txt`. Each tag should be on a new line. | `true`,`false`                                                     | `false`                                 |
| `import.local.local_path`                         | Where are the local images located?                                                                                                       | `~/import`, `./data/import`                                        | `./data/import`                         |
| `import.hydrus.enabled`                           | Should posts be imported from [hydrus](https://github.com/hydrusnetwork/hydrus)                                                           | `false`, `true`                                                    | `false`                                 |
| `import.hydrus.access_key`                        | The hydrus access key to be used                                                                                                          | `ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff` |                                         |
| `import.hydrus.url`                               | The hydrus endpoint url to be used                                                                                                        | `http://localhost:45869`, `https://192.168.0.22`                   | `http://localhost:45869/`               |
| `import.hydrus.tags`                              | The tag searches to be used                                                                                                               | `system:everything`, `system:limit is 64`                          | `system:everything`                     |
| `import.tubmlr.enabled`                           | Should posts be imported from tubmlr                                                                                                      | `true`, `false`                                                    | `false`                                 |
| `import.tubmlr.consumer_key`                      | The consumer key to be used                                                                                                               | `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF`               |                                         |
| `import.tubmlr.consumer_secret`                   | The consumer secret to be used                                                                                                            | `FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF`               |                                         |
| `import.tubmlr.blogs`                             | What blogs to import posts from                                                                                                           | `pauladrawsnstuff`, `moringmark`                                   | `pauladrawsnstuff`, `moringmark`        |
| `import.safebooru.enabled`                        | Should you import images from safebooru?                                                                                                  | `true`, `false`                                                    | `true`                                  |
| `import.safebooru.searches`                       | What tag searches to perform                                                                                                              | `overwatch rating:safe`                                            | `["asami_sato yuri -bra -bikini",...]`  |
| `import.safebooru.limit`                          | The maximum number of images to import, null for no limit                                                                                 | `1000`, `20`, `null`                                               | `null`                                  |
| `storage.method`                                  | Which method should media be stored with                                                                                                  | `s3`, `local`                                                      | `local`                                 |
| `storage.local.path`                              | The location to store local files                                                                                                         | `./data/storage`, `~/store`                                        | `./data/storage`                        |
| `storage.s3.bucket-name`                          | The bucket name to store media in, MUST BE UNIQUE                                                                                         | `openbooru` `valid-bucket-name`                                    |                                         |
| `authentication.token_expiration`                 | The amount of time in seconds before login tokens expire                                                                                  | `86400`, `null`                                                    | `null`                                  |
| `authentication.password_requirements.min_length` | The minimum acceptable length for a password                                                                                              | `8`, `4`, `12`                                                     | `8` (OWASP recommendation)              |
| `authentication.password_requirements.max_length` | The maximum acceptable length for a password (to prevent DOS attacks)                                                                     | `64`, `256`                                                        | `128`                                   |
| `authentication.password_requirements.score`      | The minimum [zxcvbn](https://github.com/dropbox/zxcvbn) score, 2 is recommended                                                           | `1`, `2`, `3`, `4`                                                 | `2`                                     |

## encoding

### Settings

Most image settings are in the encoding section share them.

#### lossless

Should the media be webp lossless

#### quality

Re-encoded webp quality (1-100/lossless)

Default: `80`

#### max_width

 max width before downscaling

#### max_height

max height before downscaling

### Thumbnail

The endoing settings for all thumbnails

### Image Full

The full sized image settings

### Image Preview

The preview image settings

### Animation

The full animation settings

## permissions

The permissions granted to certain users levels, custom levels can be created

### Options

| Name              | Description                                 |
| ----------------- | ------------------------------------------- |
| canViewUsers      | Can view other user's profiles              |
| canSearchUsers    | Can search for users                        |
| canEditUsers      | Can edit other user's accounts              |
| canDeleteUsers    | Can delete other user's accounts            |
| canCreatePosts    | Can create posts                            |
| canViewPosts      | Can view posts                              |
| canSearchPosts    | Can search for posts                        |
| canEditPosts      | Can make edits to posts                     |
| canDeletePosts    | Can delete other people's posts             |
| canCreateComments | Can create comments on posts                |
| canViewComments   | Can view other people's comments on posts   |
| canDeleteComments | Can delete other people's comments on posts |

### Levels

The default user levels are:

- Anonymous
  - Anyone can access
  - Default for unauthenticated users
- Users
  - Anyone with a user account
- Admin
  - The site owners or admins
