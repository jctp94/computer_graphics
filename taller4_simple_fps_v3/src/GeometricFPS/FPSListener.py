import PUJ_Ogre

class FPSListener( PUJ_Ogre.BaseListener ):
    def __init__( self, root, app ):
        super( FPSListener, self ).__init__( root )
        self.m_app = app
    # end def

    def mousePressed( self, evt ):
        self.m_app.shootBullet( )
        print( 'Mouse button pressed: ' + str( evt.button ) )
        return True
    # end def
# end class