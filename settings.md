# Config

These settings are mandatory

## Site

### display_name

When displaying to the user, this is the name of the api

Example: `Open Booru`, `Gelbooru`

### hostname

The hostname to use when providing links

Example: `localhost`, `api.openbooru.org`

### port

The port to host the api on

Example: `443`, `8080`

## SSL

The settings for https/ssl

### enabled

Make use of https?

### key

path to the ssl key file

### cert

path to the ssl cert file

## hcaptcha

The settings for making use of hcaptcha

### enabled

Should [hcaptcha](https://www.hcaptcha.com/) be required for verified endpoints

### sitekey

Your hcaptcha sitekey

### secret

Your hcaptcha secret key

## aws

The credentials for AWS to use

### id

Your AWS access key ID

### secret

Your AWS secret key

### region

The AWS region to use

### mongodb

### hostname

The hostname of the mongodb server

### port

The port of the mongodb server

#### name

What database name to use in mongodb

Default: `openbooru`
Options: `test`

# Settings

These settings come pre-configured, but can be changed by the user

## database

### wipe_on_startup

Wipe the database on startup, useful for testing

Default: `false`

### choice

Which database to use

Default: `mongodb`
Options: `mongodb`

## email

### template_paths

A series of paths to the email templates

#### email_verification

The email used in account signup to verify a user owns an account

Default: `"./data/emails/email_verification.html"`

#### password_reset

The email used to reset a user's password

Default: `"./data/emails/password_reset.html"`

## posts

### search

#### default_sort

The default sort method if none is specified

Default: `created_at`
Options: `id`, `created_at`, `views`, `upvotes`, `downvotes`

#### max_limit

Max number of results users a user gets per search

Default: `100`

### import

#### local

Import a set of local images. To import tags, have a file with the same name as image ending in `.txt`. Each tag should be on a new line.

##### enabled

Should local images be imported?

Default: `false`

##### local_path

Where are the local images located?

Default: `"./data/import"`

#### safebooru

Import images from safebooru

##### enabled

Should you import images from gelbooru?

Default: `true`

##### searches

What searches

Default: `["asami_sato yuri -bra -bikini",...]`

##### limit

The maximum number of images to import, null for no limit

Default: `null`

## storage

### method

Options: `local`,`s3`
Default: `local`

### local

T

#### path

### s3

Store the images on s3, requires aws credentials

#### bucket-name

What bucket name to use on s3

Default: `openbooru`

## authentication

Settings for authentication

### token_expiration

How many in seconds should tokens last for

Default: `86400`

### password_requirements

The password requirements for users

#### min_length

The minumum acceptable length of a password

Default: `8`

#### max_length

The maximum acceptable length of a password

Default: `128`

#### score

The minimum strength required for a password

1 is increibly vulnerable, 4 is very secure

Based on [zxcvbn](https://github.com/dropbox/zxcvbn)

Default: `3`

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

The permissions granted to certain users levels

### Options

| Name              | Description |
| ----------------- | --- |
| canViewUsers      | Can view other user's profiles |
| canSearchUsers    | Can search for users |
| canEditUsers      | Can edit other user's accounts |
| canDeleteUsers    | Can delete other user's accounts |
| canCreatePosts    | Can create posts |
| canViewPosts      | Can view posts |
| canSearchPosts    | Can search for posts |
| canEditPosts      | Can make edits to posts |
| canDeletePosts    | Can delete other people's posts |
| canCreateComments | Can create comments on posts |
| canViewComments   | Can view other people's comments on posts |
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
