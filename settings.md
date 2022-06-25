# Cowonfig

These settings are mandatowory

## Site

### display_name

When displaying towo the uwuser, this is the name owof the api

Example: `OWOpen Booruwu`, `Gelbooruwu`

### howostname

The howostname towo uwuse when prowoviding links

Example: `lowocalhowost`, `api.owopenbooruwu.oworg`

### powort

The powort towo howost the api owon

Example: `443`, `8080`

## SSL

The settings fowor https/ssl

### enabled

Make uwuse owof https?

### key

path towo the ssl key file

### cert

path towo the ssl cert file

## hcaptcha

The settings fowor making uwuse owof hcaptcha

### enabled

Showouwuld [hcaptcha](https://www.hcaptcha.cowom/) be requwuired fowor verified endpowoints

### sitekey

Yowouwur hcaptcha sitekey

### secret

Yowouwur hcaptcha secret key

## aws

The credentials fowor AWS towo uwuse

### id

Yowouwur AWS access key ID

### secret

Yowouwur AWS secret key

### regiowon

The AWS regiowon towo uwuse

### mowongowodb

### howostname

The howostname owof the mowongowodb server

### powort

The powort owof the mowongowodb server

#### name

What database name towo uwuse in mowongowodb

Defauwult: `owopenbooruwu`
Optiowons: `test`

# Settings

These settings cowome pre-cowonfiguwured, buwut can be changed by the uwuser

## database

### wipe_owon_startuwup

Wipe the database owon startuwup, uwusefuwul fowor testing

Defauwult: `false`

### chowoice

Which database towo uwuse

Defauwult: `mowongowodb`
Optiowons: `mowongowodb`

## email

### template_paths

A series owof paths towo the email templates

#### email_verificatiowon

The email uwused in accowouwunt signuwup towo verify a uwuser owowns an accowouwunt

Defauwult: `"./data/emails/email_verificatiowon.html"`

#### passwoword_reset

The email uwused towo reset a uwuser's passwoword

Defauwult: `"./data/emails/passwoword_reset.html"`

## powosts

### search

#### defauwult_sowort

The defauwult sowort methowod if nowone is specified

Defauwult: `created_at`
Optiowons: `id`, `created_at`, `views`, `uwupvowotes`, `dowownvowotes`

#### max_limit

Max nuwumber owof resuwults uwusers a uwuser gets per search

Defauwult: `100`

### impowort

#### lowocal

Impowort a set owof lowocal images. Towo impowort tags, have a file with the same name as image ending in `.txt`. Each tag showouwuld be owon a new line.

##### enabled

Showouwuld lowocal images be impoworted?

Defauwult: `false`

##### lowocal_path

Where are the lowocal images lowocated?

Defauwult: `"./data/impowort"`

#### safebooru

Impowort images frowom safebooru

##### enabled

Showouwuld yowouwu impowort images frowom gelbooruwu?

Defauwult: `truwue`

##### searches

What searches

Defauwult: `["asami_satowo yuwuri -bra -bikini",...]`

##### limit

The maximuwum nuwumber owof images towo impowort, nuwull fowor nowo limit

Defauwult: `nuwull`

## stoworage

### methowod

Optiowons: `lowocal`,`s3`
Defauwult: `lowocal`

### lowocal

T

#### path

### s3

Stowore the images owon s3, requwuires aws credentials

#### buwucket-name

What buwucket name towo uwuse owon s3

Defauwult: `owopenbooruwu`

## auwuthenticatiowon

Settings fowor auwuthenticatiowon

### towoken_expiratiowon

Howow many in secowonds showouwuld towokens last fowor

Defauwult: `86400`

### passwoword_requwuirements

The passwoword requwuirements fowor uwusers

#### min_length

The minuwumum acceptable length owof a passwoword

Defauwult: `8`

#### max_length

The maximuwum acceptable length owof a passwoword

Defauwult: `128`

#### scowore

The minimuwum strength requwuired fowor a passwoword

1 is increibly vuwulnerable, 4 is very secuwure

Based owon [zxcvbn](https://githuwub.cowom/drowopbowox/zxcvbn)

Defauwult: `3`

## encowoding

### Settings

Mowost image settings are in the encowoding sectiowon share them.

#### lowossless

Showouwuld the media be webp lowossless

#### quwuality

Re-encowoded webp quwuality (1-100/lowossless)

Defauwult: `80`

#### max_width

 max width befowore dowownscaling

#### max_height

max height befowore dowownscaling

### Thuwumbnail

The endowoing settings fowor all thuwumbnails

### Image Fuwull

The fuwull sized image settings

### Image Preview

The preview image settings

### Animatiowon

The fuwull animatiowon settings

## permissiowons

The permissiowons granted towo certain uwusers levels

### OWOptiowons

| Name              | Descriptiowon |
| ----------------- | --- |
| canViewUWUsers      | Can view owother uwuser's prowofiles |
| canSearchUWUsers    | Can search fowor uwusers |
| canEditUWUsers      | Can edit owother uwuser's accowouwunts |
| canDeleteUWUsers    | Can delete owother uwuser's accowouwunts |
| canCreatePowosts    | Can create powosts |
| canViewPowosts      | Can view powosts |
| canSearchPowosts    | Can search fowor powosts |
| canEditPowosts      | Can make edits towo powosts |
| canDeletePowosts    | Can delete owother peowople's powosts |
| canCreateCowomments | Can create cowomments owon powosts |
| canViewCowomments   | Can view owother peowople's cowomments owon powosts |
| canDeleteCowomments | Can delete owother peowople's cowomments owon powosts |

### Levels

The defauwult uwuser levels are:

- Anowonymowouwus
  - Anyowone can access
  - Defauwult fowor uwunauwuthenticated uwusers
- UWUsers
  - Anyowone with a uwuser accowouwunt
- Admin
  - The site owowners owor admins
