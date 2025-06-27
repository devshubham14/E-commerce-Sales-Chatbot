import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../context/AuthContext';
import { 
  FaShoppingCart, 
  FaUser, 
  FaSignOutAlt, 
  FaBars, 
  FaTimes,
  FaComments,
  FaHome,
  FaBox
} from 'react-icons/fa';

const Nav = styled.nav`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;
`;

const Logo = styled(Link)`
  font-size: 1.8rem;
  font-weight: bold;
  color: #667eea;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    color: #764ba2;
  }
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const NavLink = styled(Link)`
  color: #333;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    background: #667eea;
    color: white;
  }
`;

const AuthButtons = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const Button = styled.button`
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &.primary {
    background: #667eea;
    color: white;
    
    &:hover {
      background: #764ba2;
    }
  }
  
  &.secondary {
    background: transparent;
    color: #667eea;
    border: 2px solid #667eea;
    
    &:hover {
      background: #667eea;
      color: white;
    }
  }
`;

const CartIcon = styled(Link)`
  position: relative;
  color: #333;
  font-size: 1.2rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    background: #667eea;
    color: white;
  }
`;

const CartBadge = styled.span`
  position: absolute;
  top: -5px;
  right: -5px;
  background: #e74c3c;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #333;
  cursor: pointer;
  
  @media (max-width: 768px) {
    display: block;
  }
`;

const MobileMenu = styled.div`
  position: fixed;
  top: 80px;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(${props => props.isOpen ? '0' : '-100%'});
  transition: transform 0.3s ease;
  z-index: 999;
  
  @media (min-width: 769px) {
    display: none;
  }
`;

const MobileNavLink = styled(Link)`
  display: block;
  padding: 1rem 2rem;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    background: #f8f9fa;
  }
`;

const MobileButton = styled.button`
  width: 100%;
  padding: 1rem 2rem;
  border: none;
  background: none;
  color: #333;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-bottom: 1px solid #eee;
  
  &:hover {
    background: #f8f9fa;
  }
`;

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [cartItemCount, setCartItemCount] = useState(0);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      <Nav>
        <Logo to="/">
          <FaBox />
          E-Commerce Bot
        </Logo>
        
        <NavLinks>
          <NavLink to="/">
            <FaHome />
            Home
          </NavLink>
          <NavLink to="/products">
            <FaBox />
            Products
          </NavLink>
          {isAuthenticated && (
            <>
              <NavLink to="/chat">
                <FaComments />
                Chat
              </NavLink>
              <CartIcon to="/cart">
                <FaShoppingCart />
                Cart
                {cartItemCount > 0 && <CartBadge>{cartItemCount}</CartBadge>}
              </CartIcon>
            </>
          )}
        </NavLinks>
        
        <AuthButtons>
          {isAuthenticated ? (
            <>
              <Button className="secondary" onClick={() => navigate('/profile')}>
                <FaUser />
                {user?.username}
              </Button>
              <Button className="secondary" onClick={handleLogout}>
                <FaSignOutAlt />
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button className="secondary" onClick={() => navigate('/login')}>
                Login
              </Button>
              <Button className="primary" onClick={() => navigate('/register')}>
                Register
              </Button>
            </>
          )}
        </AuthButtons>
        
        <MobileMenuButton onClick={toggleMobileMenu}>
          {isMobileMenuOpen ? <FaTimes /> : <FaBars />}
        </MobileMenuButton>
      </Nav>
      
      <MobileMenu isOpen={isMobileMenuOpen}>
        <MobileNavLink to="/" onClick={() => setIsMobileMenuOpen(false)}>
          <FaHome />
          Home
        </MobileNavLink>
        <MobileNavLink to="/products" onClick={() => setIsMobileMenuOpen(false)}>
          <FaBox />
          Products
        </MobileNavLink>
        {isAuthenticated && (
          <>
            <MobileNavLink to="/chat" onClick={() => setIsMobileMenuOpen(false)}>
              <FaComments />
              Chat
            </MobileNavLink>
            <MobileNavLink to="/cart" onClick={() => setIsMobileMenuOpen(false)}>
              <FaShoppingCart />
              Cart
            </MobileNavLink>
            <MobileButton onClick={() => { navigate('/profile'); setIsMobileMenuOpen(false); }}>
              <FaUser />
              Profile
            </MobileButton>
            <MobileButton onClick={handleLogout}>
              <FaSignOutAlt />
              Logout
            </MobileButton>
          </>
        )}
        {!isAuthenticated && (
          <>
            <MobileButton onClick={() => { navigate('/login'); setIsMobileMenuOpen(false); }}>
              Login
            </MobileButton>
            <MobileButton onClick={() => { navigate('/register'); setIsMobileMenuOpen(false); }}>
              Register
            </MobileButton>
          </>
        )}
      </MobileMenu>
    </>
  );
};

export default Navbar; 