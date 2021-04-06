from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Project

class ProfileTestClass(TestCase):
    def setUp(self):
        self.ryan = User(username = "ryan", email = "ryan@gmail.com",password = "1234")
        self.profile = Profile(user= self.ryan, profile_pic='mepng',bio='bio', location='Nairobi, Kenya', email='ryan@gmail', link='www.profile.com')
        self.ryan.save()
        self.profile.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.ryan, User))
        self.assertTrue(isinstance(self.profile, Profile))

    def test_edit_bio(self):
        self.profile.edit_bio('I am cool')
        self.assertEqual(self.profile.bio, 'I am cool')



class ProjectTestClass(TestCase):
    def setUp(self):
        self.ryan = User(username = "ryan", email = "ryan@gmail.com",password = "1234")
        self.profile = Profile(user= self.ryan, profile_pic='mepng',bio='bio', location='Nairobi, Kenya', email='ryan@gmail', link='www.profile.com')
        self.project = Project(name= "test", screenshot = "imageurl", description ="test project", link = "testlink", profile= self.profile)

        self.ryan.save()
        self.profile.save_profile()
        self.project.save_project()

    def tearDown(self):
        Project.objects.all().delete()

    def test_image_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_project(self):
        projects = Project.objects.all()
        self.assertTrue(len(projects)> 0)

    def test_delete_project(self):
        projects1 = Project.objects.all()
        self.assertEqual(len(projects1),1)
        self.project.delete_project()
        projects2 = Project.objects.all()
        self.assertEqual(len(projects2),0)

    def test_display_projects(self):
        projects = Project.display_all_projects()
        self.assertTrue(len(projects) > 0 )

    def test_search_project(self):
        project = Project.search_project('test')
        self.assertEqual(len(project),1)

    def test_get_user_projects_(self):
        profile_projects = Project.get_user_projects(self.profile.id)
        self.assertEqual(profile_projects[0].name, 'test')
        self.assertEqual(len(profile_projects),1 )