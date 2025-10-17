#resources/site.py
from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}
    

class Site(Resource):
    def get(self,url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': "Site not found"}, 404

    def post(self,url):
        if SiteModel.find_site(url):
            return {"message": "The site '{url}' alredy exists."}, 400
        #se não rodar por seu código use o do vídeo:
        #site = SiteModel(url)
        #site.save_site() 
        try:
            site = SiteModel(url)
            site.save_site()
        except:
            return {'message': 'An internal error ocurred trying to create a new site.'}, 500
        return site.json()
    
    def delete(self,url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'site deletado com sucesso!'}
        return {'message': 'Site not found.'},404