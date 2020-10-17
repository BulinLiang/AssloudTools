from view.launcher import LauncherView
from view.app import AppView

from model.auth import AuthModel
from controller.auth import AuthController
from service.auth import AuthService

from view.product.MeeTouch import MeeTouchProductView
from model.product.MeeTouch import MeeTouchProductModel
from view.product.MeeSee import MeeSeeProductView
from model.product.MeeSee import MeeSeeProductModel
from view.product.MeeMake import MeeMakeProductView
from model.product.MeeMake import MeeMakeProductModel
from view.document.BundleEdit import BundleEditDocumentView
from model.document.BundleEdit import BundleEditDocumentModel
from view.document.AssetEdit import AssetEditDocumentView
from model.document.AssetEdit import AssetEditDocumentModel
from view.maker.PhotoAlbum import PhotoAlbumMakerView
from model.maker.PhotoAlbum import PhotoAlbumMakerModel
from view.maker.Karaoke import KaraokeMakerView
from model.maker.Karaoke import KaraokeMakerModel
from view.maker.Reciting import RecitingMakerView
from model.maker.Reciting import RecitingMakerModel
from view.maker.RingPhotography360 import RingPhotography360MakerView
from model.maker.RingPhotography360 import RingPhotography360MakerModel
from view.setting.Tools import ToolsSettingView
from model.setting.Tools import ToolsSettingModel
from view.admin.AssloudSource import AssloudSourceAdminView
from model.admin.AssloudSource import AssloudSourceAdminModel


def Register(_framework):
    authModel = AuthModel()
    _framework.modelCenter.Register(AuthModel.NAME, authModel)

    authController = AuthController()
    _framework.controllerCenter.Register(AuthController.NAME, authController)

    launcherView = LauncherView()
    _framework.viewCenter.Register(LauncherView.NAME, launcherView)
    appView = AppView()
    _framework.viewCenter.Register(AppView.NAME, appView)

    authService = AuthService()
    _framework.serviceCenter.Register(AuthService.NAME, authService)

    # Product
    # MeeTouch
    modelMeeTouchProduct = MeeTouchProductModel()
    _framework.modelCenter.Register(MeeTouchProductModel.NAME, modelMeeTouchProduct)
    viewMeeTouchProduct = MeeTouchProductView()
    _framework.viewCenter.Register(MeeTouchProductView.NAME, viewMeeTouchProduct)
    # MeeSee
    modelMeeSeeProduct = MeeSeeProductModel()
    _framework.modelCenter.Register(MeeSeeProductModel.NAME, modelMeeSeeProduct)
    viewMeeSeeProduct = MeeSeeProductView()
    _framework.viewCenter.Register(MeeSeeProductView.NAME, viewMeeSeeProduct)
    # MeeMake
    modelMeeMakeProduct = MeeMakeProductModel()
    _framework.modelCenter.Register(MeeMakeProductModel.NAME, modelMeeMakeProduct)
    viewMeeMakeProduct = MeeMakeProductView()
    _framework.viewCenter.Register(MeeMakeProductView.NAME, viewMeeMakeProduct)

    # Document
    # BundleEdit
    modelBundleEdit = BundleEditDocumentModel()
    _framework.modelCenter.Register(BundleEditDocumentModel.NAME, modelBundleEdit)
    viewBundleEdit = BundleEditDocumentView()
    _framework.viewCenter.Register(BundleEditDocumentView.NAME, viewBundleEdit)
    # AssetEdit
    modelAssetEdit = AssetEditDocumentModel()
    _framework.modelCenter.Register(AssetEditDocumentModel.NAME, modelAssetEdit)
    viewAssetEdit = AssetEditDocumentView()
    _framework.viewCenter.Register(AssetEditDocumentView.NAME, viewAssetEdit)

    # Maker
    # PhotoAlbum
    modelPhotoAlbumMaker = PhotoAlbumMakerModel()
    _framework.modelCenter.Register(PhotoAlbumMakerModel.NAME, modelPhotoAlbumMaker)
    viewPhotoAlbumMaker = PhotoAlbumMakerView()
    _framework.viewCenter.Register(PhotoAlbumMakerView.NAME, viewPhotoAlbumMaker)
    #  Karaoke
    modelKaraokeMaker = KaraokeMakerModel()
    _framework.modelCenter.Register(KaraokeMakerModel.NAME, modelKaraokeMaker)
    viewKaraokeMaker = KaraokeMakerView()
    _framework.viewCenter.Register(KaraokeMakerView.NAME, viewKaraokeMaker)
    #  Reciting 
    modelRecitingMaker = RecitingMakerModel()
    _framework.modelCenter.Register(RecitingMakerModel.NAME, modelRecitingMaker)
    viewRecitingMaker = RecitingMakerView()
    _framework.viewCenter.Register(RecitingMakerView.NAME, viewRecitingMaker)
    #  RingPhotography360
    modelRingPhotography360 = RingPhotography360MakerModel()
    _framework.modelCenter.Register(RingPhotography360MakerModel.NAME, modelRingPhotography360)
    viewRingPhotography360 = RingPhotography360MakerView()
    _framework.viewCenter.Register(RingPhotography360MakerView.NAME, viewRingPhotography360)

    # Setting
    # Template

    # Tools
    modelTools = ToolsSettingModel()
    _framework.modelCenter.Register(ToolsSettingModel.NAME, modelTools)
    viewTools = ToolsSettingView()
    _framework.viewCenter.Register(ToolsSettingView.NAME, viewTools)

    # Admin
    # AssloudSource
    modelAssloudSource = AssloudSourceAdminModel()
    _framework.modelCenter.Register(AssloudSourceAdminModel.NAME, modelAssloudSource)
    viewAssloudSource = AssloudSourceAdminView()
    _framework.viewCenter.Register(AssloudSourceAdminView.NAME, viewAssloudSource)

def Cancel(_framework):
    # 视图中心
    _framework.viewCenter.Cancel(MeeMakeProductView.NAME)
    _framework.viewCenter.Cancel(MeeSeeProductView.NAME)
    _framework.viewCenter.Cancel(MeeTouchProductView.NAME)
    _framework.viewCenter.Cancel(BundleEditDocumentView.NAME)
    _framework.viewCenter.Cancel(AssetEditDocumentView.NAME)
    _framework.viewCenter.Cancel(RingPhotography360MakerView.NAME)
    _framework.viewCenter.Cancel(RecitingMakerView.NAME)
    _framework.viewCenter.Cancel(KaraokeMakerView.NAME)
    _framework.viewCenter.Cancel(PhotoAlbumMakerView.NAME)
    _framework.viewCenter.Cancel(ToolsSettingView.NAME)
    _framework.viewCenter.Cancel(AssloudSourceAdminView.NAME)
    _framework.viewCenter.Cancel(LauncherView.NAME)
    _framework.viewCenter.Cancel(AppView.NAME)
    # 控制中心
    _framework.controllerCenter.Cancel(AuthController.NAME)
    # 数据中心
    _framework.modelCenter.Cancel(AuthModel.NAME)
    _framework.modelCenter.Cancel(MeeTouchProductModel.NAME)
    _framework.modelCenter.Cancel(MeeSeeProductModel.NAME)
    _framework.modelCenter.Cancel(MeeMakeProductModel.NAME)
    _framework.modelCenter.Cancel(BundleEditDocumentModel.NAME)
    _framework.modelCenter.Cancel(AssetEditDocumentModel.NAME)
    _framework.modelCenter.Cancel(PhotoAlbumMakerModel.NAME)
    _framework.modelCenter.Cancel(KaraokeMakerModel.NAME)
    _framework.modelCenter.Cancel(RecitingMakerModel.NAME)
    _framework.modelCenter.Cancel(RingPhotography360MakerModel.NAME)
    _framework.modelCenter.Cancel(ToolsSettingModel.NAME)
    _framework.modelCenter.Cancel(AssloudSourceAdminModel.NAME)
    # 服务中心
    _framework.serviceCenter.Cancel(AuthService.NAME)
