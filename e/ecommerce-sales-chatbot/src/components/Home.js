import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../context/AuthContext';
import { FaArrowRight, FaComments, FaShoppingCart, FaStar } from 'react-icons/fa';
import axios from 'axios';

const HomeContainer = styled.div`
  min-height: 100vh;
  color: white;
`;

const Hero = styled.section`
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
  }
`;

const HeroContent = styled.div`
  z-index: 1;
  max-width: 800px;
  padding: 0 2rem;
`;

const HeroTitle = styled.h1`
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const HeroSubtitle = styled.p`
  font-size: 1.3rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
  
  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
`;

const CTAButtons = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
`;

const CTAButton = styled(Link)`
  padding: 1rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &.primary {
    background: white;
    color: #667eea;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
  }
  
  &.secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
    
    &:hover {
      background: white;
      color: #667eea;
      transform: translateY(-2px);
    }
  }
`;

const Features = styled.section`
  padding: 4rem 2rem;
  background: white;
  color: #333;
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const FeatureCard = styled.div`
  text-align: center;
  padding: 2rem;
  border-radius: 15px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const FeatureIcon = styled.div`
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 1rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
`;

const FeatureDescription = styled.p`
  color: #666;
  line-height: 1.6;
`;

const FeaturedProducts = styled.section`
  padding: 4rem 2rem;
  background: #f8f9fa;
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #333;
`;

const ProductsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const ProductCard = styled.div`
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const ProductImage = styled.div`
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
`;

const ProductInfo = styled.div`
  padding: 1.5rem;
`;

const ProductName = styled.h3`
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #333;
`;

const ProductPrice = styled.p`
  font-size: 1.3rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 1rem;
`;

const ProductDescription = styled.p`
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
`;

const ViewButton = styled(Link)`
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 0.9rem;
  transition: background 0.3s ease;
  
  &:hover {
    background: #764ba2;
  }
`;

const Home = () => {
  const { isAuthenticated } = useAuth();
  const [featuredProducts, setFeaturedProducts] = useState([]);

  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        const response = await axios.get('/api/products?limit=6');
        setFeaturedProducts(response.data.slice(0, 6));
      } catch (error) {
        console.error('Error fetching featured products:', error);
      }
    };

    fetchFeaturedProducts();
  }, []);

  return (
    <HomeContainer>
      <Hero>
        <HeroContent>
          <HeroTitle>Welcome to E-Commerce Bot</HeroTitle>
          <HeroSubtitle>
            Discover amazing products with the help of our intelligent chatbot assistant. 
            Get personalized recommendations, find the perfect items, and enjoy a seamless shopping experience.
          </HeroSubtitle>
          <CTAButtons>
            {isAuthenticated ? (
              <>
                <CTAButton to="/chat" className="primary">
                  <FaComments />
                  Start Chatting
                  <FaArrowRight />
                </CTAButton>
                <CTAButton to="/products" className="secondary">
                  Browse Products
                  <FaArrowRight />
                </CTAButton>
              </>
            ) : (
              <>
                <CTAButton to="/register" className="primary">
                  Get Started
                  <FaArrowRight />
                </CTAButton>
                <CTAButton to="/login" className="secondary">
                  Sign In
                  <FaArrowRight />
                </CTAButton>
              </>
            )}
          </CTAButtons>
        </HeroContent>
      </Hero>

      <Features>
        <SectionTitle>Why Choose Our Platform?</SectionTitle>
        <FeaturesGrid>
          <FeatureCard>
            <FeatureIcon>
              <FaComments />
            </FeatureIcon>
            <FeatureTitle>AI-Powered Chatbot</FeatureTitle>
            <FeatureDescription>
              Get instant help and personalized product recommendations from our intelligent chatbot assistant.
            </FeatureDescription>
          </FeatureCard>
          <FeatureCard>
            <FeatureIcon>
              <FaShoppingCart />
            </FeatureIcon>
            <FeatureTitle>Easy Shopping</FeatureTitle>
            <FeatureDescription>
              Browse products, manage your cart, and complete purchases with just a few clicks.
            </FeatureDescription>
          </FeatureCard>
          <FeatureCard>
            <FeatureIcon>
              <FaStar />
            </FeatureIcon>
            <FeatureTitle>Quality Products</FeatureTitle>
            <FeatureDescription>
              Discover a wide range of high-quality products across various categories.
            </FeatureDescription>
          </FeatureCard>
        </FeaturesGrid>
      </Features>

      <FeaturedProducts>
        <SectionTitle>Featured Products</SectionTitle>
        <ProductsGrid>
          {featuredProducts.map((product) => (
            <ProductCard key={product.id}>
              <ProductImage>
                {product.name.charAt(0)}
              </ProductImage>
              <ProductInfo>
                <ProductName>{product.name}</ProductName>
                <ProductPrice>${product.price}</ProductPrice>
                <ProductDescription>
                  {product.description.length > 100 
                    ? `${product.description.substring(0, 100)}...` 
                    : product.description}
                </ProductDescription>
                <ViewButton to={`/products/${product.id}`}>
                  View Details
                </ViewButton>
              </ProductInfo>
            </ProductCard>
          ))}
        </ProductsGrid>
      </FeaturedProducts>
    </HomeContainer>
  );
};

export default Home; 