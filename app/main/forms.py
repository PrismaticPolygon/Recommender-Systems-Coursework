import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from load import season, weekend
from location import get_location

from app.models import Country


class ContextForm(FlaskForm):

    countries = [(164, 'Afghanistan'), (170, 'Albania'), (125, 'Algeria'), (133, 'Andorra'), (140, 'Angola'),
                 (160, 'Anguilla'), (85, 'Antigua and Barbuda'), (55, 'Argentina'), (60, 'Armenia'), (30, 'Australia'),
                 (64, 'Austria'), (101, 'Azerbaijan'), (47, 'Bahrain'), (99, 'Bangladesh'), (58, 'Barbados'),
                 (57, 'Belarus'), (24, 'Belgium'), (127, 'Benin'), (118, 'Bolivia'), (27, 'Botswana'), (0, 'Brazil'),
                 (130, 'British Virgin Islands'), (89, 'Brunei'), (36, 'Brunei Darussalam'), (112, 'Bulgaria'),
                 (152, 'Burkina Faso'), (146, 'Cambodia'), (67, 'Cameroon'), (5, 'Canada'), (70, 'Cayman Islands'),
                 (26, 'Chile'), (69, 'China'), (44, 'Colombia'), (163, 'Congo'), (77, 'Costa Rica'), (31, 'Croatia'),
                 (132, 'Cyprus'), (53, 'Czech Republic'), (162, 'Democratic Republic of Congo'), (41, 'Denmark'),
                 (169, 'Dominica'), (54, 'Dominican Republic'), (73, 'Ecuador'), (49, 'Egypt'), (76, 'El Salvador'),
                 (161, 'Equatorial Guinea'), (61, 'Estonia'), (176, 'Ethiopia'), (154, 'Falkland Islands'),
                 (95, 'Fiji'), (51, 'Finland'), (4, 'France'), (177, 'French Polynesia'), (115, 'French-Guiana'),
                 (144, 'Gabon'), (136, 'Georgia'), (18, 'Germany'), (25, 'Ghana'), (102, 'Gibraltar'), (39, 'Greece'),
                 (167, 'Grenada'), (107, 'Guadeloupe'), (82, 'Guatemala'), (138, 'Guyana'), (103, 'Haiti'),
                 (84, 'Honduras'), (52, 'Hong Kong-China'), (35, 'Hungary'), (94, 'Iceland'), (34, 'India'),
                 (1, 'Indonesia'), (172, 'Iran'), (92, 'Iraq'), (19, 'Ireland'), (106, 'Israel'), (21, 'Italy'),
                 (135, 'Ivory Coast'), (79, 'Jamaica'), (16, 'Japan'), (65, 'Jordan'), (72, 'Kazakhstan'), (8, 'Kenya'),
                 (48, 'Kuwait'), (83, 'Kyrgyzstan'), (22, 'Lebanon'), (131, 'Lesotho'), (159, 'Libya'),
                 (93, 'Luxemburg'), (171, 'Macau-China'), (98, 'Macedonia'), (149, 'Madagascar'), (109, 'Malawi'),
                 (6, 'Malaysia'), (100, 'Maldives'), (158, 'Mali'), (90, 'Malta'), (105, 'Martinique'),
                 (179, 'Mauritania'), (143, 'Mauritius'), (175, 'Mayotte'), (11, 'Mexico'), (88, 'Moldova'),
                 (155, 'Monaco'), (142, 'Mongolia'), (108, 'Montenegro'), (32, 'Morocco'), (145, 'Mozambique'),
                 (150, 'Myanmar'), (81, 'Namibia'), (129, 'Nepal'), (141, 'Netherlands Antilles'), (46, 'New Zealand'),
                 (96, 'Nicaragua'), (29, 'Nigeria'), (165, 'North Korea'), (40, 'Norway'), (71, 'Oman'),
                 (86, 'Pakistan'), (151, 'Palestinian Territories'), (59, 'Panama'), (75, 'Paraguay'), (50, 'Peru'),
                 (7, 'Philippines'), (33, 'Poland'), (43, 'Portugal'), (91, 'Qatar'), (23, 'Republic of Latvia'),
                 (78, 'Republic of Lithuania'), (122, 'Reunion'), (80, 'Romania'), (15, 'Russia'), (139, 'Rwanda'),
                 (178, 'Saint Kitts and Nevis'), (134, 'Saint Vincent and the Grenadines'), (168, 'Saint-Martin'),
                 (153, 'Samoa'), (68, 'Saudi Arabia'), (128, 'Senegal'), (126, 'Serbia'), (173, 'Sierra Leone'),
                 (12, 'Singapore'), (157, 'Slovakia'), (111, 'Slovenia'), (120, 'Somalia'), (17, 'South Africa'),
                 (62, 'South Korea'), (20, 'Spain'), (87, 'Sri Lanka'),
                 (148, 'St Helena Ascension and Tristan da Cunha'), (147, 'St. Lucia'), (113, 'Sudan'),
                 (121, 'Suriname'), (110, 'Swaziland'), (10, 'Sweden'), (56, 'Switzerland'), (117, 'Syria'),
                 (63, 'Taiwan'), (116, 'Tanzania'), (28, 'Thailand'), (66, 'The Bahamas'), (119, 'The Gambia'),
                 (14, 'The Netherlands'), (166, 'Togo'), (74, 'Trinidad and Tobago'), (124, 'Tunisia'),
                 (9, 'Turkey'), (123, 'Turks and Caicos Islands'), (37, 'Uganda'), (38, 'Ukraine'),
                 (42, 'United Arab Emirates'), (2, 'United Kingdom'), (3, 'United States'), (137, 'Uruguay'),
                 (104, 'Uzbekistan'), (156, 'Vatican City State'), (45, 'Venezuela'), (13, 'Vietnam'), (97, 'Zambia'),
                 (114, 'Zimbabwe')
    ]   # Cribbed from the DB
    seasons = [(1, "Spring"), (2, "Summer"), (3, "Autumn"), (0, "Winter")]   # See load.py
    weekends = [(1, "True"), (0, "False")]

    dt = datetime.datetime.today()

    x = get_location()
    country_id = None

    for country in countries:

        if country[1] == x:

            country_id = country[0]

    if country_id is None:  # Default to UK

        country_id = 2

    country_options = SelectMultipleField(
         u'Select country', choices=countries, coerce=int, validators=[DataRequired()], default=[country_id]
    )

    season_options = SelectMultipleField(
        u'Select season', choices=seasons, coerce=int, validators=[DataRequired()], default=[season(dt.month)]
    )

    weekend_options = SelectMultipleField(
        u'Select weekend', choices=weekends, coerce=int, validators=[DataRequired()], default=[weekend(dt.weekday())]
    )

    submit = SubmitField('Submit')



