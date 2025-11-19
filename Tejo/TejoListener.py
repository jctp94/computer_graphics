import PUJ_Ogre

class TejoListener( PUJ_Ogre.BaseListener ):
    def __init__( self, root, app ):
        super( TejoListener, self ).__init__( root )
        self.m_app = app
    # end def

    def mousePressed( self, evt ):
        self.m_app.throwTejo( )
        print( 'Mouse button pressed: ' + str( evt.button ) )
        return True
    # end def
# end class